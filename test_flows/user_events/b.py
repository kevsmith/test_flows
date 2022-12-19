from metaflow import FlowSpec, trigger_on, step


@trigger_on(events=["my.other.event"])
class BFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("B done")


if __name__ == "__main__":
    BFlow()
