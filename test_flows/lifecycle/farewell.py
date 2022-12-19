from metaflow import FlowSpec, step, trigger_on_finish


@trigger_on_finish(flow="HelloFlow")
class FarewellFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Fare thee well")


if __name__ == "__main__":
    FarewellFlow()
