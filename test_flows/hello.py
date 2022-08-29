import os

from metaflow import FlowSpec, step, trigger_after

@trigger_after(flow="GoodbyeFlow")
class HelloFlow(FlowSpec):

    @step
    def start(self):
        # Event.start_flow(flow="GoodbyeFlow").send()
        self.next(self.foo)

    @step
    def foo(self):
        self.next(self.end)

    @step
    def end(self):
        print("Hello")

if __name__ == "__main__":
    HelloFlow()