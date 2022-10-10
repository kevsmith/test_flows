from metaflow import FlowSpec, trigger_on, step


# @trigger_on(event="my-other-event")
class BarFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Foo done")


if __name__ == "__main__":
    BarFlow()
