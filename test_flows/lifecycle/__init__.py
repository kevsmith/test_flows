from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    tests.append(Test(rs["goodbye.py"], rs["hello.py"]))
    tests[-1].add_case(
        f"[{__package__}] triggers on success lifecycle event", "hello.py", "goodbye.py"
    )

    tests.append(Test(rs["hello_ns.py"], rs["goodbye_ns.py"]))
    tests[-1].add_case(
        f"[{__package__}] (@project) triggers on success lifecycle event",
        "hello_ns.py",
        "goodbye_ns.py",
    )

    tests.append(Test(rs["foo.py"], rs["bar.py"], rs["baz.py"]))
    tests[-1].add_case(
        f"[{__package__}] triggers on multiple success lifecycle events",
        ["foo.py", "bar.py"],
        "baz.py",
    )

    tests.append(Test(rs["foo_ns.py"], rs["bar_ns.py"], rs["baz_ns.py"]))
    tests[-1].add_case(
        f"[{__package__}] (@project) triggers on multiple success lifecycle events",
        ["foo_ns.py", "bar_ns.py"],
        "baz_ns.py",
    )
    return tests
