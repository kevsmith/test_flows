from metaflow import FlowSpec, trigger_on, step, current


def assert_eq(expected, value, message=None):
    if expected != value:
        if message is None:
            raise RuntimeError(f"Expected {expected} but have {value}")
        else:
            raise RuntimeError(f"{message}\nExpected {expected} but have {value}")


@trigger_on(
    events=["giraffe.user.kevsmith.an.event", "giraffe.user.kevsmith.another.event"]
)
class DownstreamNsFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        assert_eq(2, len(current.trigger), "Triggering events")
        print("Done")


if __name__ == "__main__":
    DownstreamNsFlow()
