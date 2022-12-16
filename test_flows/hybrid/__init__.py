from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    t = Test(*rs, prefix=__package__)
    t.add_case(
        "triggers on lifecycle and user events and passes param",
        ["foo.py", "bar.py"],
        "baz.py",
    )
    # t.add_case(
    #     "(@project) triggers on lifecycle and user events and passes param",
    #     ["foo_ns.py", "bar_ns.py"],
    #     "baz_ns.py",
    # )
    tests.append(t)
    return tests
