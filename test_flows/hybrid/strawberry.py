from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter


@trigger_on(flows=["AppleFlow"], event="banana.is.running")
class StrawberryFlow(FlowSpec):
    score = Parameter(name="score", required=True, type=int)

    @step
    def start(self):
        if self.score != 100:
            raise RuntimeError("Expected score to be 100; have %d" % self.score)
        self.next(self.end)

    @step
    def end(self):
        print("StrawberryFlow done")


if __name__ == "__main__":
    StrawberryFlow()
