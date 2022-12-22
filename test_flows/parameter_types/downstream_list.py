from metaflow import FlowSpec, step, trigger_on, current
from metaflow.parameters import Parameter


def assert_eq(expected, value, message=None):
    if expected != value:
        if message is None:
            raise RuntimeError(f"Expected {expected} but have {value}")
        else:
            raise RuntimeError(f"{message}\nExpected {expected} but have {value}")


@trigger_on(events=["downstream.lists"], mappings={"value": "my_list"})
class DownstreamListFlow(FlowSpec):
    value = Parameter(name="value", type=list)

    @step
    def start(self):
        assert_eq(1, len(current.trigger), "Triggering events")
        expected = ["a", "b", 1, 2, 3.45]
        if self.value != expected:
            raise RuntimeError(f"Expected value {expected}; got {self.value}")
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    DownstreamListFlow()
