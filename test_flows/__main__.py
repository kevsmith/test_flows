from datetime import datetime
import random
import sys

from test_flows import lifecycle, parameters, raw_events
from test_flows.flow_tester import run_tests

from kubernetes import config


def main(args):
    config.load_kube_config()
    random.seed(int(datetime.utcnow().timestamp()))
    all_tests = []
    if len(args) == 0:
        all_tests = lifecycle.tests(tests=all_tests)
        all_tests = parameters.tests(tests=all_tests)
        all_tests = raw_events.tests(tests=all_tests)
    else:
        seen = []
        for arg in args:
            if arg in seen:
                print(f"Ignoring duplicate {arg}")
                continue
            if arg == "lifecycle":
                all_tests = lifecycle.tests(tests=all_tests)
                print(f"Added {arg} tests")
                seen.append(arg)
            elif arg == "parameters":
                all_tests = parameters.tests(tests=all_tests)
                print(f"Added {arg} tests")
                seen.append(arg)
            elif arg == "raw_events":
                all_tests = raw_events.tests(tests=all_tests)
                print(f"Added {arg} tests")
                seen.append(arg)
    random.shuffle(all_tests)
    run_tests(all_tests)


if __name__ == "__main__":
    main(sys.argv[1:])
