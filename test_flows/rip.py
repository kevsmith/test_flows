from metaflow import FlowSpec, step, trigger_on


@trigger_on(flow="HelloFlow", status="failed")
class RestInPeaceFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Rest in peace")


if __name__ == "__main__":
    RestInPeaceFlow()
