from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    t = Test(*rs, prefix=__package__)

    t.add_case("triggers on success lifecycle event", "hello.py", "goodbye.py")

    t.add_case(
        "(@project) triggers on success lifecycle event",
        "hello_ns.py",
        "goodbye_ns.py",
    )

    t.add_case(
        "triggers on multiple success lifecycle events",
        ["foo.py", "bar.py"],
        "baz.py",
    )

    t.add_case(
        "(@project) triggers on multiple success lifecycle events",
        ["foo_ns.py", "bar_ns.py"],
        "baz_ns.py",
    )

    t.add_case(
        "triggers on namespaced flow finish signal from outside namespace",
        "hello_ns.py",
        "snooper.py",
    )

    tests.append(t)
    return tests
