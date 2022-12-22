from metaflow import FlowSpec, step, trigger_on, current
from metaflow.parameters import Parameter
from test_flows.util import assert_eq


@trigger_on(flows=["AppleFlow"], events=["banana.is.running"])
class StrawberryFlow(FlowSpec):
    score = Parameter(name="score", required=True, type=int)

    @step
    def start(self):
        assert_eq(2, len(current.trigger), "Triggering events")
        if self.score != 100:
            raise RuntimeError("Expected score to be 100; have %d" % self.score)
        self.next(self.end)

    @step
    def end(self):
        print("StrawberryFlow done")


if __name__ == "__main__":
    StrawberryFlow()
