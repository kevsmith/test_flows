from metaflow import FlowSpec, step, trigger_on_finish, project


@trigger_on_finish(flows=["HelloFlow"])
@project(name="kevsmith_test")
class FarewellFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Fare thee well")


if __name__ == "__main__":
    FarewellFlow()
