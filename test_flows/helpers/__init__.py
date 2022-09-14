import glob
import subprocess
import random
from os import path
from sys import stdin, stderr


def flow_path(caller, flow):
    prefix = path.dirname(caller)
    if not flow.endswith(".py"):
        flow = f"{flow}.py"
    return path.join(prefix, flow)


def runners_from_files(caller):
    prefix = path.dirname(caller)
    runners = {}
    for f in glob.glob(f"{prefix}/*.py"):
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
        t.run()

    passed = True

    for t in tests:
        if not t.report(verbose=True):
            passed = False

    if not passed:
        print("\nResult: FAIL\n\n")
    else:
        print("\nResult: PASS\n\n")


class Command:
    def __init__(self, cmd):
        if type(cmd) == str:
            self.commands = cmd.split(" ")
        else:
            self.commands = cmd

    def execute(self):
        result = subprocess.run(self.commands, stdout=subprocess.DEVNULL)
        return result

    def must(self):
        self.execute().check_returncode()

    def should(self):
        return self.execute().returncode == 0


class FlowRunner:
    def __init__(self, flow):
        self.name = path.basename(flow)
        self.deleter = Command(["python", flow, "--quiet", "argo-workflows", "delete"])
        self.creator = Command(["python", flow, "--quiet", "argo-workflows", "create"])
        self.starter = Command(["python", flow, "--quiet", "argo-workflows", "trigger"])

    def setup(self):
        print(f"Setting up {self.name}")
        self.deleter.should()
        self.creator.must()

    def run(self):
        print(f"Starting {self.name}")
        self.starter.must()

    def cleanup(self):
        print(f"Cleaning up {self.name}")
        self.deleter.should()


class TestCase:
    def __init__(self, name, trigger, targets, should_run, should_succeed):
        self.name = name
        self.trigger = trigger
        self.targets = targets
        self.should_run = should_run
        self.should_succeed = should_succeed
        self.passed = False

    def prompt(self, runners):
        others = [
            key
            for key in runners.keys()
            if key not in self.targets and key != self.trigger
        ]
        answer = "n"
        if self.should_run:
            if self.should_succeed:
                answer = input(
                    f"Did the {', '.join(self.targets)} {pluralize(self.targets, 'flow', 'flows')} run and succeed (y/n)? "
                ).lower()
                if answer in ["y", "yes"] and len(others) > 0:
                    answer = input(
                        f"Did {pluralize(others, 'flow', 'flows')} {', '.join(others)} NOT run (y/n)? "
                    ).lower()
            else:
                answer = input(f"Did {self.target} flow run and fail (y/n)? ").lower()
        else:
            answer = input(f"Did {self.target} flow NOT run (y/n)? ").lower()
        return answer in ["y", "yes"]

    def run(self, runners):
        header = ""
        while len(header) < len(f"Testing case {self.name}"):
            header = f"{header}-"
        print(f"\n\nTesting case {self.name}\n{header}", flush=True)
        runners[self.trigger].run()
        self.passed = self.prompt(runners)
        return self.passed


class Test:
    def __init__(self, *args):
        self.runners = {}
        for runner in args:
            self.runners[runner.name] = runner
        self.cases = []

    def setup(self):
        try:
            for name in self.runners.keys():
                self.runners[name].setup()
        except Exception as e:
            for name in self.runners.keys():
                self.runners[name].cleanup()
            raise e

    def add_case(self, name, trigger_flow, targets, should_run=True, succeeded=True):
        if type(targets) == str:
            targets = [targets]
        self.cases.append(TestCase(name, trigger_flow, targets, should_run, succeeded))

    def run(self):
        self.setup()
        random.shuffle(self.cases)
        try:
            for case in self.cases:
                case.run(self.runners)
        finally:
            for name in self.runners.keys():
                self.runners[name].cleanup()

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
