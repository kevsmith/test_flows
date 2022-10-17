from metaflow import FlowSpec, trigger_on, step


@trigger_on(event="my.event")
class FooFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Foo done")


if __name__ == "__main__":
    FooFlow()
