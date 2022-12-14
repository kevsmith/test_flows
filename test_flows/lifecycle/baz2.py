from metaflow import FlowSpec, step, trigger_on_finish


@trigger_on_finish(flows=["FooFlow", "BarFlow"])
class Baz2Flow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("BazFlow done")


if __name__ == "__main__":
    Baz2Flow()
