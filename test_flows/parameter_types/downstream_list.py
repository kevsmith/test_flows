from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter


@trigger_on(events=["downstream.lists"], mappings={"value": "my_list"})
class DownstreamListFlow(FlowSpec):
    value = Parameter(name="value", type=list)

    @step
    def start(self):
        expected = ["a", "b", 1, 2, 3.45]
        if self.value != expected:
            raise RuntimeError(f"Expected value {expected}; got {self.value}")
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    DownstreamListFlow()
