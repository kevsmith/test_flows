from metaflow import FlowSpec, step, trigger_on, project
from metaflow.parameters import Parameter


@project(name="coelacanth")
@trigger_on(flow="FooFlow", event="bar.is.running")
class BazFlow(FlowSpec):
    score = Parameter(name="score", required=True, type=int)

    @step
    def start(self):
        if self.score != 100:
            raise RuntimeError("Expected score to be 100; have %d" % self.score)
        self.next(self.end)

    @step
    def end(self):
        print("BazFlow done")


if __name__ == "__main__":
    BazFlow()
