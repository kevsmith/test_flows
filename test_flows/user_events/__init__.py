from test_flows.flow_tester import Test, runners_from_files, run_tests


def tests(tests=[]):
    rs = runners_from_files(__file__)

    t = Test(*rs)
    t.add_case(
        f"[{__package__}] triggers multiple flows using user events",
        "three_way.py",
        ["foo.py", "bar.py", "baz.py"],
    )
    t.add_case(
        f"[{__package__}] (@project) triggers multiple flows using user events",
        "three_way_ns.py",
        ["foo_ns.py", "baz_ns.py"],
    )
    tests.append(t)
    return tests
