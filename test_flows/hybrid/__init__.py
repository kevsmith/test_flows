from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    t = Test(*rs, prefix=__package__)
    t.add_case(
        "triggers on lifecycle and user events and passes param",
        ["apple.py", "banana.py"],
        "strawberry.py",
    )
    t.add_case(
        "(@project) triggers on lifecycle and user events and passes param",
        ["apple_ns.py", "banana_ns.py"],
        "strawberry_ns.py",
    )
    tests.append(t)
    return tests
