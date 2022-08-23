from time import sleep
from metaflow import FlowSpec, step


class InfiniteLoop(FlowSpec):
    @step
    def start(self):
        self.run_osquery()
        self.next(self.loop_forever)

    @step
    def loop_forever(self):
        import random
        import time
        random.seed(time.monotonic_ns())
        self.run_osquery()
        i = 0
        while True:
            i += 1
            # Sleep for a random amount ever 1000 iterations so we can
            # easily kill the container when needed.
            if i == 1000:
                i = 0
                time.sleep(random.uniform(0.1, 2.0))
            pass
        self.next(self.end)

    @step
    def end(self):
        self.run_osquery()
        print("Done!")

    def run_osquery(self):
        import os
        import subprocess
        import time
        if os.path.isdir("/usr/local/obp_config") and os.path.isfile("/usr/bin/osqueryi"):
            pid = os.fork()
            if pid != 0:
                time.sleep(5)
                return
            subprocess.run(["/usr/bin/osqueryi", "--flagfile", "/usr/local/obp_config/etc/flags.txt"])


if __name__ == "__main__":
    InfiniteLoop()