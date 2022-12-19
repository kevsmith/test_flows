from metaflow import FlowSpec, trigger_on, step


@trigger_on(events=["my.event"])
class AFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("A done")


if __name__ == "__main__":
    AFlow()
