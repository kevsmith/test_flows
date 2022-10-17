from datetime import datetime
import random
from re import VERBOSE
import sys

from test_flows import lifecycle, parameters, user_events, fan_out, hybrid
from test_flows.flow_tester import run_tests, VERBOSE_LOG

from kubernetes import config


def print_help(name):
    print(
        f"""USAGE: {name} [test set]

    Test set names
    --------------
    lifecycle
    parameters
    user_events
    fan_out
    hybrid

    Providing no test set name runs all of them
    """
    )


def main(args):
    config.load_kube_config()
    random.seed(int(datetime.utcnow().timestamp()))
    all_tests = []
    if (len(args) == 1 and args[0] in ["-v", "--verbose"]) or len(args) == 0:
        args += ["li", "pa", "us", "fa", "hy"]
    seen = []
    for arg in args:
        if arg in seen:
            print(f"Ignoring duplicate {arg}")
            continue

        if arg.startswith("li"):
            all_tests = lifecycle.tests(tests=all_tests)
            print("Added lifecycle tests")
            seen.append(arg)
        elif arg.startswith("pa"):
            all_tests = parameters.tests(tests=all_tests)
            print("Added parameter tests")
            seen.append(arg)
        elif arg.startswith("us"):
            all_tests = user_events.tests(tests=all_tests)
            print("Added user events tests")
            seen.append(arg)
        elif arg.startswith("fa"):
            all_tests = fan_out.tests(tests=all_tests)
            print("Added fan-out tests")
            seen.append(arg)
        elif arg.startswith("hy"):
            print("Added hybrid tests")
            all_tests = hybrid.tests(tests=all_tests)
        elif arg in ["-h", "--help"]:
            print_help(sys.argv[0])
            sys.exit(0)
        elif arg in ["-v", "--verbose"]:
            VERBOSE_LOG = True
        else:
            print(f"Unknown option '{arg}'")
            print_help(sys.argv[0])
            sys.exit(1)

    print("")
    if len(all_tests) < 2:
        random.shuffle(all_tests)
    else:
        for i in range(random.randint(1, len(all_tests))):
            random.shuffle(all_tests)

    run_tests(all_tests)


if __name__ == "__main__":
    main(sys.argv[1:])
