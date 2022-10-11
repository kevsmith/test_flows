from metaflow import FlowSpec, step, trigger_on


class BarFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("BarFlow done")


if __name__ == "__main__":
    BarFlow()
