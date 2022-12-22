from datetime import datetime, timedelta
import glob
import os
import random
from multiprocessing import Pool
from os import getenv, path
import threading
from time import sleep

from kubernetes import client
import requests

from .cluster import FlowFinder, FlowRunner, SearchTimeoutError


MD_URL = "http://localhost:8081"

HEADERS = {"x-api-key": getenv("METAFLOW_API_KEY")}


def shuffle(items):
    import random

    random.seed(int(datetime.timestamp(datetime.utcnow())))
    if len(items) < 2:
        return items
    elif len(items) == 2:
        random.shuffle(items)
    else:
        times = int(len(items) / 2) + 1
        for i in range(times):
            random.shuffle(items)
    return items


def wait_for_status(flows, desired):
    final_statuses = ["Succeeded", "Failed", "Error"]
    final_statuses.remove(desired)
    finalists = []
    skipped = []
    while len(finalists) + len(skipped) < len(flows):
        for flow in flows:
            if flow.id in finalists or flow.id in skipped:
                continue
            flow.wait_and_refresh()
            if flow.status == desired:
                finalists.append(flow.id)
            elif flow.status in final_statuses:
                skipped.append(flow.id)
    return len(finalists) == len(flows)


def flow_path(caller, flow):
    prefix = path.dirname(caller)
    if not flow.endswith(".py"):
        flow = f"{flow}.py"
    return path.join(prefix, flow)


def runners_from_files(caller):
    prefix = path.dirname(caller)
    runners = []
    files = sorted([f for f in glob.glob(f"{prefix}/*.py") if f.find("__") == -1])
    for f in files:
        runner = FlowRunner(flow_path(caller, f))
        runners.append(runner)
    return runners


def pluralize(things, singular, plural):
    if len(things) < 2:
        return singular
    else:
        return plural


def run_tests(tests, reporter):
    test_count = len(tests)
    suite = None
    for t in tests:
        if suite is None:
            suite = t.prefix
        t.run(reporter)

    passed = True

    for t in tests:
        if not t.report():
            passed = False

    reporter.final_status(suite, passed)


def setup_runner(runner):
    sleep(random.random() * 2.0)
    runner.setup(None)


def start_runner(runner):
    run = runner[0].run(runner[1])
    run.wait_and_refresh()
    return run


class Reporter:
    def start_test_case(self, name):
        pass

    def all_flows_started(self):
        pass

    def all_expected_flows_succeeded(self, status):
        pass

    def verify_metadata(self, status):
        pass

    def finish_test_case(self, status, reason=None):
        pass

    def final_status(self, name, status):
        pass

    def output(self, text):
        print(text, end="", flush=True)

    def output_line(self, text):
        print(text, flush=True)


class CLIReporter(Reporter):
    def start_test_case(self, name):
        header = name
        while len(header) < 96:
            header = f"{header}."
        self.output(header)

    def all_flows_started(self):
        self.output(".")

    def all_expected_flows_succeeded(self, status):
        if status:
            self.output(".")
        else:
            self.output("!")

    def verify_metadata(self, status):
        if status:
            self.output(".")
        else:
            self.output("!")

    def finish_test_case(self, status, reason=None):
        if status:
            self.output_line("PASS")
        else:
            self.output_line("FAIL")
            if reason is not None and len(reason) > 0:
                self.output_line(f"Missing: {','.join(reason)}")

    def final_status(self, name, status):
        header = name
        while len(header) < 98:
            header = f"{header}."
        if status:
            header += "PASS"
        else:
            header += "FAIL"
        self.output_line(header)


class TestCase:
    def __init__(self, name, triggers, targets):
        self.name = name
        if type(triggers) == str:
            self.triggers = [triggers]
        else:
            self.triggers = triggers
        self.targets = targets
        self.passed = False

    def run(self, runners, reporter):
        reporter.start_test_case(self.name)
        flows = self._start_flows(runners)
        reporter.all_flows_started()
        min_started_at = datetime.utcnow()
        missing = []
        for s in flows:
            if s and s.started_at < min_started_at:
                min_started_at = s.started_at
        try:
            finder = FlowFinder(self.targets, min_started_at, len(self.targets) * 150)
            while not finder.has_found_all():
                finder.wait_and_refresh()
            flows = flows + finder.found
            self.passed = wait_for_status(flows, "Succeeded")
        except SearchTimeoutError as e:
            if len(e.missing) > 0:
                missing += e.missing
                self.passed = False
            else:
                self.passed = True
        reporter.all_expected_flows_succeeded(self.passed)
        reporter.finish_test_case(self.passed, reason=missing)

    def _start_flows(self, runners):
        pending = []
        for target in self.targets:
            if type(target) == tuple:
                runner = runners[target[0]]
                runner.setup(target[1])
        for trigger in self.triggers:
            if type(trigger) == tuple:
                runner = runners[trigger[0]]
                runner.setup(trigger[1])
                pending.append((runner, trigger[1]))
            else:
                pending.append((runners[trigger], None))
        return [start_runner(runner) for runner in pending]

    def _req(self, url):
        resp = requests.get(url=url, headers=HEADERS)
        resp.raise_for_status()
        return resp.json()

    def _verify_metadata(self):
        flows = [class_name_from_file(target) for target in self.targets]

        def sorter(x):
            if "timestamp" in x:
                return x["timestamp"]
            elif "ts_epoch" in x:
                return x["ts_epoch"]
            else:
                print(x.keys())
                raise RuntimeError("Required key missing")

        for flow in flows:
            runs = self._req(f"{MD_URL}/flows/{flow}/runs")
            tries = 0
            while len(runs) == 0 and tries < 5:
                tries += 1
                sleep(1)
                runs = self._req(f"{MD_URL}/flows/{flow}/runs")
            if len(runs) == 0:
                print(f"No run metadata found for flow {flow}!")
                return False
            last_run = sorted(runs, key=sorter, reverse=True)[0]
            task = sorted(
                self._req(
                    f"{MD_URL}/flows/{flow}/runs/{last_run['run_number']}/steps/start/tasks"
                ),
                key=sorter,
                reverse=True,
            )[0]
            all_md = self._req(
                f"{MD_URL}/flows/{flow}/runs/{last_run['run_number']}/steps/start/tasks/{task['task_id']}/metadata"
            )
            if len([m for m in all_md if m["type"] == "trigger_events"]) == 0:
                return False
        return True


class Test:
    def __init__(self, *args, prefix=""):
        self.runners = {}
        for runner in args:
            self.runners[runner.name] = runner
        self.cases = []
        self.prefix = prefix

    def setup(self):
        pool = Pool(processes=os.cpu_count())
        names = self.runners.keys()
        pending = [self.runners[name] for name in names]
        pool.map(setup_runner, pending)
        pool.close()
        pool.join()
        self._compile_log()
        print(f"Starting {self.prefix} tests ({len(self.cases)})", flush=True)

    def _compile_log(self):
        names = glob.glob("FLOW_NAME_*")
        contents = []

        def key(item):
            if item.find(".") > -1:
                return (len(item), item)
            else:
                return (0, item)

        with open("FLOW_NAMES", "w+") as master_file:
            for line in master_file.readlines():
                contents.append(line)
            for name in names:
                with open(name, "r") as fd:
                    new_lines = fd.readlines()
                    for new_name in new_lines:
                        if new_name not in contents:
                            contents.append(new_name)
                os.remove(name)
            contents.sort(key=key, reverse=True)
            master_file.truncate()
            master_file.writelines(contents)

    def add_case(self, name, trigger_flow, targets):
        if self.prefix != "":
            name = f"[{self.prefix}] {name}"
        if type(targets) == str:
            targets = [targets]
        self.cases.append(TestCase(name, trigger_flow, targets))

    def run(self, reporter):
        self.setup()
        self.cases = shuffle(self.cases)
        for case in self.cases:
            case.run(self.runners, reporter)

    def _format_case_name(self, case_name):
        while len(case_name) < 55:
            case_name = f"{case_name}."
        return case_name

    def report(self):
        passed = 0
        for case in self.cases:
            if case.passed:
                passed += 1
        return passed == len(self.cases)
