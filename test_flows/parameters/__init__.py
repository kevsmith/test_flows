from test_flows.flow_tester import Test, runners_from_files


def tests(tests=[]):
    rs = runners_from_files(__file__)

    t = Test(*rs, prefix=__package__)

    t.add_case(
        "triggers on user event & passes param",
        "short.py",
        "parameters.py",
    )
    t.add_case(
        "(@project) triggers on user event & passes param",
        "short_ns.py",
        "parameters_ns.py",
    )
    t.add_case(
        "triggers on user events from multiple flows & passes params",
        ["given_name.py", "surname.py"],
        "full_name.py",
    )
    t.add_case(
        "(@project) triggers on user events from multiple flows & passes params",
        ["given_name_ns.py", "surname_ns.py"],
        "full_name_ns.py",
    )
    t.add_case(
        "triggers on a user event and maps multiple params",
        ["message.py"],
        "template.py",
    )

    tests.append(t)
    return tests
