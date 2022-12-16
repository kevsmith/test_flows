from metaflow import FlowSpec, trigger_on, step
from metaflow.parameters import Parameter


@trigger_on(event="my.other.other.event")
class CFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("C done")


if __name__ == "__main__":
    CFlow()
