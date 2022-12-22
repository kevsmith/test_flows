from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    t = Test(*rs, prefix=__package__)

    # test_types = ["string", "int", "float", "list", "dict", "json"]
    # test_types = ["string", "int", "float", "list"]
    test_types = ["string", "int", "float"]

    for tt in test_types:
        t.add_case(
            f"passes {tt} parameters correctly",
            f"upstream_{tt}.py",
            f"downstream_{tt}.py",
        )
        t.add_case(
            f"(@project) passes {tt} parameters correctly",
            f"upstream_{tt}_ns.py",
            f"downstream_{tt}ns.py",
        )

    tests.append(t)
    return tests
