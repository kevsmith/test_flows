from test_flows.helpers import Test, runners_from_files, run_tests


def tests(tests=[]):
    rs = runners_from_files(__file__)

    tests.append(Test(rs["parameters.py"], rs["short.py"], rs["parameters_ns.py"]))
    tests[-1].add_case("triggers & passes param", "short.py", "parameters.py")

    tests.append(Test(rs["parameters_ns.py"], rs["short_ns.py"], rs["parameters.py"]))
    tests[-1].add_case("(NS) triggers & pass param", "short_ns.py", "parameters_ns.py")

    return tests
