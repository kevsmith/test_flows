from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    t = Test(*rs)
    t.add_case(
        f"[{__package__}] triggers on lifecycle and user events and passes param",
        ["foo.py", "bar.py"],
        "baz.py",
    )
    t.add_case(
        f"[{__package__}] (@project) triggers on lifecycle and user events and passes param",
        ["foo.py", "bar.py"],
        "baz.py",
    )
    tests.append(t)
    return tests
