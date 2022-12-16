from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    t = Test(*rs, prefix=__package__)
    t.add_case(
        "triggers multiple flows using user events",
        "three_way.py",
        ["foo.py", "bar.py", "quux.py"],
    )
    t.add_case(
        "(@project) triggers multiple flows using user events",
        "three_way_ns.py",
        ["foo_ns.py", "bar_ns.py", "quux_ns.py"],
    )
    tests.append(t)
    return tests
