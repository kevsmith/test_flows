from datetime import datetime
import random
from re import VERBOSE
import sys

from test_flows import (
    lifecycle,
    parameters,
    user_events,
    hybrid,
    reset,
    parameter_types,
)
from test_flows.flow_tester import run_tests, CLIReporter

from kubernetes import config


def print_help(name):
    print(
        f"""USAGE: {name} [test set]

    Test set names
    --------------
    hybrid
    lifecycle
    parameters
    reset
    user_events

    Providing no test set name runs all of them
    """
    )


def clear_work_files():
    import glob
    import os

    names = glob.glob("FLOW_NAME_*")
    for name in names:
        os.remove(name)


def main(args):
    clear_work_files()
    config.load_kube_config()
    t = int(datetime.timestamp(datetime.now()))
    random.seed(t)
    min_t = int(t / 2)
    max_t = t
    t += random.randint(min_t, max_t)
    random.seed(t)
    all_tests = []
    if len(args) == 0:
        args = ["hy", "li", "pa", "re", "us", "ty"]
    seen = []
    for arg in args:
        if arg in seen:
            print(f"Ignoring duplicate {arg}")
            continue

        if arg.startswith("li"):
            all_tests = lifecycle.tests(tests=all_tests)
            seen.append(arg)
        elif arg.startswith("pa"):
            all_tests = parameters.tests(tests=all_tests)
            seen.append(arg)
        elif arg.startswith("us"):
            all_tests = user_events.tests(tests=all_tests)
            seen.append(arg)
        elif arg.startswith("re"):
            all_tests = reset.tests(tests=all_tests)
            seen.append(arg)
        elif arg.startswith("ty"):
            all_tests = parameter_types.tests(tests=all_tests)
            seen.append(arg)
        elif arg.startswith("hy"):
            all_tests = hybrid.tests(tests=all_tests)
        elif arg in ["-h", "--help"]:
            print_help(sys.argv[0])
            sys.exit(0)
        else:
            print(f"Unknown option '{arg}'")
            print_help(sys.argv[0])
            sys.exit(1)

    print("")
    if len(all_tests) < 4:
        random.shuffle(all_tests)
    else:
        for i in range(random.randint(1, len(all_tests))):
            random.shuffle(all_tests)

    reporter = CLIReporter()
    run_tests(all_tests, reporter)


if __name__ == "__main__":
    main(sys.argv[1:])
