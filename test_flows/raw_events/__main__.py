from test_flows.helpers import Test, runners_from_files, run_tests

rs = runners_from_files(__file__)
tests = []

tests.append(Test(rs["three_way.py"], rs["foo.py"], rs["bar.py"], rs["baz.py"]))
tests[-1].add_case(
    "triggered by raw events", "three_way.py", ["foo.py", "bar.py", "baz.py"]
)

tests.append(
    Test(rs["three_way_ns.py"], rs["foo_ns.py"], rs["bar.py"], rs["baz_ns.py"])
)
tests[-1].add_case(
    "ns triggered by raw events", "three_way_ns.py", ["foo_ns.py", "baz_ns.py"]
)
run_tests(tests)
