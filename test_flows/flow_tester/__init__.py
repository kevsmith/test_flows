from datetime import datetime, timedelta
import glob
import subprocess
import random
import re
from os import path
from time import sleep

from kubernetes import client

from .cluster import FlowFinder, FlowRunner


def wait_for_status(flows, desired):
    final_statuses = ["Succeeded", "Failed", "Error"].remove(desired)
    finalists = []
    skipped = []
    while len(finalists) + len(skipped) < len(flows):
        for flow in flows:
            if flow.id in finalists:
                continue
            flow.wait_until_refresh()
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
    runners = {}
    files = sorted([f for f in glob.glob(f"{prefix}/*.py") if f.find("__") == -1])
    for f in files:
        runner = FlowRunner(flow_path(caller, f))
        runners[runner.name] = runner
    return runners


def pluralize(things, singular, plural):
    if len(things) < 2:
        return singular
    else:
        return plural


def run_tests(tests):
    for t in tests:
        result = "r"
        while result == "r":
            result = t.run()

    passed = True

    for t in tests:
        if not t.report(verbose=True):
            passed = False

    if not passed:
        print("\nResult: FAIL\n\n")
    else:
        print("\nResult: PASS\n\n")


class TestCase:
    def __init__(self, name, triggers, targets, should_run, should_succeed):
        self.name = name
        if type(triggers) == str:
            self.triggers = [triggers]
        else:
            self.triggers = triggers
        self.targets = targets
        self.should_run = should_run
        self.should_succeed = should_succeed
        self.passed = False

    def run(self, runners):
        header = ""
        while len(header) < len(f"Case: {self.name}"):
            header = f"{header}-"
        print(f"\n\nCase: {self.name}\n{header}", flush=True)
        flows = self._start_flows(runners)
        min_started_at = datetime.utcnow()
        for s in flows:
            if s.started_at < min_started_at:
                min_started_at = s.started_at
        try:
            finder = FlowFinder(self.targets, min_started_at, len(self.targets) * 300)
            while not finder.has_found_all():
                finder.wait_until_refresh()
                finder.refresh()
            for f in finder.found:
                flows.append(f)
            self.passed = wait_for_status(flows, "Succeeded")
        except TimeoutError:
            self.passed = False

    def _start_flows(self, runners):
        runs = []
        for name in self.triggers:
            run = runners[name].run()
            run.refresh()
            print(run)
            runs.append(run)
        return runs


class Test:
    def __init__(self, *args):
        self.runners = {}
        for runner in args:
            self.runners[runner.name] = runner
        self.cases = []

    def setup(self):
        for name in self.runners.keys():
            self.runners[name].setup()

    def add_case(self, name, trigger_flow, targets, should_run=True, succeeded=True):
        if type(targets) == str:
            targets = [targets]
        self.cases.append(TestCase(name, trigger_flow, targets, should_run, succeeded))

    def run(self):
        self.setup()
        random.shuffle(self.cases)
        for case in self.cases:
            case.run(self.runners)

    def _format_case_name(self, case_name):
        while len(case_name) < 55:
            case_name = f"{case_name}."
        return case_name

    def report(self, verbose=False):
        passed = 0
        for case in self.cases:
            if case.passed:
                passed += 1
            if verbose:
                formatted = self._format_case_name(case.name)
                if case.passed:
                    print(f"{formatted}PASS")
                else:
                    print(f"{formatted}FAIL")
        return passed == len(self.cases)
