from metaflow import FlowSpec, trigger_on, step
from metaflow.parameters import Parameter


@trigger_on(
    events=["my-other-event", "my-other-other-event"],
    mappings={"my-other-event": {"entity": "person"}},
)
class BazFlow(FlowSpec):

    person = Parameter(name="person", required=True, type=str)

    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Foo done")


if __name__ == "__main__":
    BazFlow()
