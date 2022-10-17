from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    t = Test(*rs)
    t.add_case(
        f"[{__package__}] triggers on success lifecycle event", "hello.py", "goodbye.py"
    )

    t.add_case(
        f"[{__package__}] (@project) triggers on success lifecycle event",
        "hello_ns.py",
        "goodbye_ns.py",
    )

    t.add_case(
        f"[{__package__}] triggers on multiple success lifecycle events",
        ["foo.py", "bar.py"],
        "baz.py",
    )

    t.add_case(
        f"[{__package__}] (@project) triggers on multiple success lifecycle events",
        ["foo_ns.py", "bar_ns.py"],
        "baz_ns.py",
    )
    tests.append(t)
    return tests
