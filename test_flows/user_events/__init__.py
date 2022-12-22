from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    t = Test(*rs, prefix=__package__)
    t.add_case(
        "triggers multiple flows from single upstream via events",
        "three_way.py",
        ["a.py", "b.py", "d.py"],
    )
    tests.append(t)
    t.add_case("triggers flow with multiple events", "upstream.py", "downstream.py")
    t.add_case(
        "(@project) triggers flow with multiple events",
        "upstream_ns.py",
        "downstreamns.py",
    )
    return tests
