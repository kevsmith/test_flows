from os import path
import subprocess
from test_flows.flow_tester import Test, runners_from_files

FAN_OUT = 10


def tests(tests=[]):
    script_path = path.dirname(__file__)
    script = path.join(script_path, "generate.sh")
    rc = subprocess.call(["/bin/sh", script, f"{FAN_OUT}"])
    if rc != 0:
        raise RuntimeError(f"Failed to generate fan out flows: {rc}")
    rs = runners_from_files(__file__)
    dependents = [r.name for r in rs]
    dependents.remove("head_flow.py")
    t = Test(*rs)
    t.add_case(
        f"[{__package__}] trigger {FAN_OUT}-wide fan out", "head_flow.py", dependents
    )
    tests.append(t)
    return tests
