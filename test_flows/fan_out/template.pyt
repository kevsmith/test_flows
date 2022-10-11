from metaflow import FlowSpec, trigger_on, step


@trigger_on(flow="HeadFlow")
class FlowNameFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("FlowNameFlow done")


if __name__ == "__main__":
    FlowNameFlow()
