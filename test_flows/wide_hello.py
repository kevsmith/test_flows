import os
from time import sleep

from metaflow import FlowSpec, step


class WideHelloFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.foo)

    @step
    def foo(self):
        self.values = range(100)
        self.next(self.double, foreach="values")

    @step
    def double(self):
        self.doubled = self.input * 2
        for i in range(1000000):
            pass
            sleep(0.05)
        self.next(self.join)

    @step
    def join(self, inputs):
        self.final_value = sum([x.doubled for x in inputs])
        self.next(self.end)

    @step
    def end(self):
        print(f"The answer is {self.final_value}")


if __name__ == "__main__":
    WideHelloFlow()
