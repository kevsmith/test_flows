from metaflow import FlowSpec, step, trigger_on, project


@trigger_on(flow="HelloFlow", status="failed")
@project(name="kevsmith_test")
class RestInPeaceFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Rest in peace")


if __name__ == "__main__":
    RestInPeaceFlow()
