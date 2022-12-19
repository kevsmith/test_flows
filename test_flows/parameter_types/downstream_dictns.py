from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter


@trigger_on(
    events=["koala.user.kevsmith.downstream.dicts"], mappings={"value": "my_dict"}
)
class DownstreamDictNsFlow(FlowSpec):
    value = Parameter(name="value", type=dict)

    @step
    def start(self):
        expected = {"a": "b", "c": 123, "d": {"a": 456.789}}
        if self.value != expected:
            raise RuntimeError(f"Expected value {expected}; got {self.value}")
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    DownstreamDictNsFlow()
