from test_flows.flow_tester import Test, runners_from_files, run_tests


def tests(tests=[]):
    rs = runners_from_files(__file__)

    tests.append(
        Test(
            rs["three_way.py"],
            rs["foo.py"],
            rs["bar.py"],
            rs["baz.py"],
        )
    )
    tests[-1].add_case(
        f"[{__package__}] triggers multiple flows using user events",
        "three_way.py",
        ["foo.py", "bar.py", "baz.py"],
    )

    tests.append(
        Test(rs["three_way_ns.py"], rs["foo_ns.py"], rs["bar_ns.py"], rs["baz_ns.py"])
    )
    tests[-1].add_case(
        f"[{__package__}] (@project) triggers multiple flows using user events",
        "three_way_ns.py",
        ["foo_ns.py", "baz_ns.py"],
    )
    return tests
