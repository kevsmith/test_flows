from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter


@trigger_on(events=["downstream.strings"], mappings={"name": "my_string"})
class DownstreamStringFlow(FlowSpec):
    text = Parameter(name="name", type=str)

    @step
    def start(self):
        if self.text != "abc":
            raise RuntimeError(f"Expected text value 'abc'; got {self.text}")
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    DownstreamStringFlow()
