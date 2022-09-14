from unicodedata import name
from metaflow import FlowSpec, step


class HelloFlow(FlowSpec):
    @step
    def start(self):
        1 / 0
        self.next(self.end)

    @step
    def end(self):
        print("Hello")


if __name__ == "__main__":
    HelloFlow()
