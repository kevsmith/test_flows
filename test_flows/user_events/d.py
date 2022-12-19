from metaflow import FlowSpec, trigger_on, step


@trigger_on(events=["my.other.other.event"])
class DFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("D done")


if __name__ == "__main__":
    DFlow()
