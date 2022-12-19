from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter


@trigger_on(events=["downstream.ints"], mapping={"value": "my_int"})
class DownstreamIntFlow(FlowSpec):
    value = Parameter(name="value", type=int)

    @step
    def start(self):
        if self.value != 123:
            raise RuntimeError(f"Expected value 123; got {self.value}")
        self.next(self.end)

    @step
    def end(self):
        print("Done")
