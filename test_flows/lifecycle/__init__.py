from test_flows.helpers import Test, runners_from_files, run_tests


def tests(tests=[]):
    rs = runners_from_files(__file__)

    tests.append(Test(rs["goodbye.py"], rs["hello.py"]))
    tests[-1].add_case("success lifecycle event", "hello.py", "goodbye.py")

    tests.append(Test(rs["hello_ns.py"], rs["goodbye_ns.py"]))
    tests[-1].add_case(
        "(@project) success lifecycle event", "hello_ns.py", "goodbye_ns.py"
    )
    return tests
