from test_flows.helpers import Test, runners_from_files, run_tests


def tests(tests=[]):
    rs = runners_from_files(__file__)

    tests.append(Test(*(rs.values())))
    t = tests[-1]
    t.add_case("triggers & passes param", "short.py", "parameters.py")
    t.add_case("(NS) triggers & pass param", "short_ns.py", "parameters_ns.py")
    t.add_case("populate params from lifecycle annotation", "hello.py", "goodbye.py")
    t.add_case(
        "(NS) populate params from lifecycle annotation", "hello_ns.py", "goodbye_ns.py"
    )
    t.add_case(
        "populate and map params from lifecycle annotation",
        "hello_mapper.py",
        "goodbye_mapper.py",
    )

    return tests
