from test_flows.flow_tester import Test, runners_from_files, run_tests


def tests(tests=[]):
    rs = runners_from_files(__file__)

    tests.append(
        Test(
            rs["three_way.py"],
            rs["foo.py"],
            rs["bar.py"],
            rs["baz.py"],
            rs["foo_ns.py"],
        )
    )
    tests[-1].add_case(
        f"[{__package__}] trigger by raw events",
        "three_way.py",
        ["foo.py", "bar.py", "baz.py"],
    )

    tests.append(
        Test(rs["three_way_ns.py"], rs["foo_ns.py"], rs["bar.py"], rs["baz_ns.py"])
    )
    tests[-1].add_case(
        f"[{__package__}] (@project) triggered by raw events",
        "three_way_ns.py",
        ["foo_ns.py", "baz_ns.py"],
    )
    return tests
