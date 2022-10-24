from datetime import datetime, timedelta
import glob
import json
import os
import random
from multiprocessing import Pool
from os import getenv, path
from time import sleep

from kubernetes import client
import requests

from .cluster import FlowFinder, FlowRunner, SearchTimeoutError
from .util import class_name_from_file

MD_URL = "http://localhost:8081"

HEADERS = {"x-api-key": getenv("METAFLOW_API_KEY")}


def shuffle(items):
    import random

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


def run_tests(tests):
    test_count = len(tests)
    for t in tests:
        result = "r"
        while result == "r":
            result = t.run()

    passed = True

    for t in tests:
        if not t.report():
            passed = False

    if not passed:
        print("\nResult: FAIL\n\n")
    else:
        print("\nResult: PASS\n\n")


def setup_runner(runner):
    sleep(random.random() * 2)
    runner.setup()


def start_runner(runner):
    run = runner.run()
    run.wait_and_refresh()
    return run


class TestCase:
    def __init__(self, name, triggers, targets):
        self.name = name
        if type(triggers) == str:
            self.triggers = [triggers]
        else:
            self.triggers = triggers
        self.targets = targets
        self.passed = False

    def run(self, runners):
        header = f"{self.name}"
        while len(header) < 96:
            header = f"{header}."
        print(header, end="", flush=True)
        flows = self._start_flows(runners)
        print(".", end="", flush=True)
        min_started_at = datetime.utcnow()
        missing = []
        for s in flows:
            if s.started_at < min_started_at:
                min_started_at = s.started_at
        try:
            finder = FlowFinder(self.targets, min_started_at, len(self.targets) * 120)
            while not finder.has_found_all():
                finder.wait_and_refresh()
            flows = flows + finder.found
            self.passed = wait_for_status(flows, "Succeeded")
        except SearchTimeoutError as e:
            missing += e.missing
            self.passed = False
        if self.passed:
            print(".", end="", flush=True)
            self.passed = self._verify_metadata()
        else:
            print("!", end="", flush=True)
        if self.passed:
            print("PASS", flush=True)
        else:
            print("FAIL", flush=True)
            if len(missing) == 1:
                print(f"Missing workflow: {missing[0]}")
            elif len(missing) > 1:
                print(f"Missing workflows: {', '.join(missing)}")

    def _start_flows(self, runners):
        pending = [runners[name] for name in self.triggers]
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
            last_run = sorted(
                self._req(f"{MD_URL}/flows/{flow}/runs"), key=sorter, reverse=True
            )[0]
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
        if len(names) > 1:
            print(f"Deployed {', '.join(names)}")
        else:
            print(f"Deployed {names[0]}")
        if len(self.cases) > 1:
            print(f"Starting {self.prefix} tests", flush=True)
        else:
            print(f"Starting {self.prefix} test", flush=True)

    def add_case(self, name, trigger_flow, targets):
        if self.prefix != "":
            name = f"[{self.prefix}] {name}"
        if type(targets) == str:
            targets = [targets]
        self.cases.append(TestCase(name, trigger_flow, targets))

    def run(self):
        self.setup()
        self.cases = shuffle(self.cases)
        for case in self.cases:
            case.run(self.runners)

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
