from metaflow import FlowSpec, step, trigger_on, project


@trigger_on(flow="HelloFlow")
@project(name="kevsmith_test")
class FareTheeWellFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Fare thee well")


if __name__ == "__main__":
    FareTheeWellFlow()
