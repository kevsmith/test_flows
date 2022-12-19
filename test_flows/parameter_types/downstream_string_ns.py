from metaflow import FlowSpec, step, trigger_on, project
from metaflow.parameters import Parameter


@trigger_on(
    events=["koala.user.kevsmith.downstream.strings"], mapping={"name": "my_string"}
)
class DownstreamStringNsFlow(FlowSpec):
    text = Parameter(name="name", type=str)

    @step
    def start(self):
        if self.text != "abc":
            raise RuntimeError(f"Expected text value 'abc'; got {self.text}")
        self.next(self.end)

    @step
    def end(self):
        print("Done")
