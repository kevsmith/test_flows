from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    tests.append(Test(rs["foo.py"], rs["bar.py"], rs["baz.py"]))
    tests[-1].add_case(
        f"[{__package__}] triggers on lifecycle and user events and passes param",
        ["foo.py", "bar.py"],
        "baz.py",
    )

    tests.append(Test(rs["foo_ns.py"], rs["bar_ns.py"], rs["baz_ns.py"]))
    tests[-1].add_case(
        f"[{__package__}] (@project) triggers on lifecycle and user events and passes param",
        ["foo.py", "bar.py"],
        "baz.py",
    )
    return tests
