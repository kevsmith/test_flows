import os

from metaflow import FlowSpec, step, trigger_after

@trigger_after(flow="GoodbyeFlow")
class ShortFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Done")

if __name__ == "__main__":
    ShortFlow()