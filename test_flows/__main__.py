from datetime import datetime
import random
import sys

from test_flows import lifecycle, parameters, raw_events, fan_out, hybrid
from test_flows.flow_tester import run_tests

from kubernetes import config


def main(args):
    config.load_kube_config()
    random.seed(int(datetime.utcnow().timestamp()))
    all_tests = []
    if len(args) == 0:
        args = ["lifecycle", "parameters", "raw_events"]
        args.sort()
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
        elif arg == "fan_out":
            all_tests = fan_out.tests(tests=all_tests)
            print(f"Added {arg} tests")
            seen.append(arg)
        elif arg == "hybrid":
            all_tests = hybrid.tests(tests=all_tests)

    print("")
    if len(all_tests) < 2:
        random.shuffle(all_tests)
    else:
        for i in range(random.randint(1, len(all_tests))):
            random.shuffle(all_tests)

    run_tests(all_tests)


if __name__ == "__main__":
    main(sys.argv[1:])
