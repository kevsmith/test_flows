from test_flows.flow_tester import Test, runners_from_files, run_tests


def tests(tests=[]):
    rs = runners_from_files(__file__)

    tests.append(Test(rs["short.py"], rs["parameters.py"]))
    tests[-1].add_case(
        f"[{__package__}] triggers & passes param from user event",
        "short.py",
        "parameters.py",
    )
    tests.append(Test(rs["short_ns.py"], rs["parameters_ns.py"], rs["goodbye.py"]))
    tests[-1].add_case(
        f"[{__package__}] (@project) triggers & passes params from user event",
        "short_ns.py",
        "parameters_ns.py",
    )

    tests.append(Test(rs["full_name.py"], rs["surname.py"], rs["given_name.py"]))
    tests[-1].add_case(
        f"[{__package__}] populate params from multiple flow runs",
        ["given_name.py", "surname.py"],
        "full_name.py",
    )
    tests.append(
        Test(rs["full_name_ns.py"], rs["surname_ns.py"], rs["given_name_ns.py"])
    )
    tests[-1].add_case(
        f"[{__package__}] (@project) populate params from multiple flow runs",
        ["given_name_ns.py", "surname_ns.py"],
        "full_name_ns.py",
    )

    return tests
