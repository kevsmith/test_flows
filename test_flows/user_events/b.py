from metaflow import FlowSpec, trigger_on, step, current


def assert_eq(expected, value, message=None):
    if expected != value:
        if message is None:
            raise RuntimeError(f"Expected {expected} but have {value}")
        else:
            raise RuntimeError(f"{message}\nExpected {expected} but have {value}")


@trigger_on(events=["my.other.event"])
class BFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        assert_eq(1, len(current.trigger), "Triggering events")
        print("B done")


if __name__ == "__main__":
    BFlow()
