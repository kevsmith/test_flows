from unicodedata import name
from metaflow import FlowSpec, step, project


@project(name="flounder")
class BarFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("BarFlow done")


if __name__ == "__main__":
    BarFlow()
