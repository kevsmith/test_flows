from test_flows.helpers import Test, runners_from_files, run_tests


def tests(tests=[]):
    rs = runners_from_files(__file__)

    tests.append(Test(rs["goodbye.py"], rs["hello.py"]))
    tests[-1].add_case("success lifecycle event", "hello.py", "goodbye.py")

    tests.append(Test(rs["hello_err.py"], rs["goodbye.py"], rs["rip.py"]))
    tests[-1].add_case("failure lifecycle event", "hello_err.py", "rip.py")

    tests.append(Test(rs["hello_ns.py"], rs["goodbye_ns.py"], rs["rip_ns.py"]))
    tests[-1].add_case("(NS) success lifecycle event", "hello_ns.py", "goodbye_ns.py")

    tests.append(
        Test(rs["hello_ns_err.py"], rs["goodbye_ns.py"], rs["rip_ns.py"], rs["rip.py"])
    )
    tests[-1].add_case("(NS) failure lifecycle event", "hello_ns_err.py", "rip_ns.py")
    return tests
