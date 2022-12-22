from metaflow import FlowSpec, step, trigger_on, current
from metaflow.parameters import Parameter


def assert_eq(expected, value, message=None):
    if expected != value:
        if message is None:
            raise RuntimeError(f"Expected {expected} but have {value}")
        else:
            raise RuntimeError(f"{message}\nExpected {expected} but have {value}")


@trigger_on(events=["downstream.strings"], mappings={"name": "my_string"})
class DownstreamStringFlow(FlowSpec):
    text = Parameter(name="name", type=str)

    @step
    def start(self):
        assert_eq(1, len(current.trigger), "Triggering events")
        if self.text != "abc":
            raise RuntimeError(f"Expected text value 'abc'; got {self.text}")
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    DownstreamStringFlow()
