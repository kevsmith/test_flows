import os

from metaflow import FlowSpec, step


class WideHelloFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.foo)

    @step
    def foo(self):
        self.values = range(10)
        self.next(self.double, foreach="values")

    @step
    def double(self):
        self.doubled = self.input * 2
        self.next(self.join)

    @step
    def join(self, inputs):
        total = 0
        for i in inputs:
            total += i
        self.final_value = total
        self.next(self.end)

    @step
    def end(self):
        print(f"The answer is {self.final_value}")

if __name__ == "__main__":
    WideHelloFlow()