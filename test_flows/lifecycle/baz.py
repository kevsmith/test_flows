from metaflow import FlowSpec, step, trigger_on


@trigger_on(flows=["FooFlow", "BarFlow"])
class BazFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("BazFlow done")


if __name__ == "__main__":
    BazFlow()
