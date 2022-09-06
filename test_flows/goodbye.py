from unicodedata import name
from metaflow import FlowSpec, step, trigger_on


@trigger_on(flow="HelloFlow")
class GoodbyeFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Goodbye")


if __name__ == "__main__":
    GoodbyeFlow()
