from metaflow import FlowSpec, trigger_on, step, current


def assert_eq(expected, value, message=None):
    if expected != value:
        if message is None:
            raise RuntimeError(f"Expected {expected} but have {value}")
        else:
            raise RuntimeError(f"{message}\nExpected {expected} but have {value}")


@trigger_on(events=["an.event", "another.event"])
class DownstreamFlow(FlowSpec):
    @step
    def start(self):
        assert_eq(2, len(current.trigger), "Triggering events")
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    DownstreamFlow()
