from metaflow import FlowSpec, step, trigger_on, current
from metaflow.parameters import Parameter


def assert_eq(expected, value, message=None):
    if expected != value:
        if message is None:
            raise RuntimeError(f"Expected {expected} but have {value}")
        else:
            raise RuntimeError(f"{message}\nExpected {expected} but have {value}")


@trigger_on(
    events=["koala.user.kevsmith.downstream.ints"], mappings={"value": "my_int"}
)
class DownstreamIntNsFlow(FlowSpec):
    value = Parameter(name="value", type=int)

    @step
    def start(self):
        assert_eq(1, len(current.trigger), "Triggering events")
        if self.value != 123:
            raise RuntimeError(f"Expected value 123; got {self.value}")
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    DownstreamIntNsFlow()
