import os

from metaflow import FlowSpec, step

class GoodbyeFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Goodbye")

if __name__ == "__main__":
    GoodbyeFlow()