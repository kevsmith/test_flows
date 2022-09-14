from datetime import datetime
import random

from test_flows import lifecycle, parameters, raw_events
from test_flows.helpers import run_tests

all_tests = lifecycle.tests()
all_tests = parameters.tests(tests=all_tests)
all_tests = raw_events.tests(tests=all_tests)

random.seed(int(datetime.utcnow().timestamp()))
random.shuffle(all_tests)
run_tests(all_tests)
