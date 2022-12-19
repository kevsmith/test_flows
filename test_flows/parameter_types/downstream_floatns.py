from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter


@trigger_on(
    events=["koala.user.kevsmith.downstream.floats"], mappings={"value": "my_float"}
)
class DownstreamFloatNsFlow(FlowSpec):
    value = Parameter(name="value", type=float)

    @step
    def start(self):
        if self.value != 123.456:
            raise RuntimeError(f"Expected value 123.456; got {self.value}")
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    DownstreamFloatNsFlow()
