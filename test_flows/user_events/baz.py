from metaflow import FlowSpec, trigger_on, step
from metaflow.parameters import Parameter


@trigger_on(event="my.other.other.event")
class BazFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Baz done")


if __name__ == "__main__":
    BazFlow()
