from metaflow import FlowSpec, step, trigger_on, project



@trigger_on(flow="HelloFlow")
@project(name="kevsmith_test")
class GoodbyeFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Goodbye")


if __name__ == "__main__":
    GoodbyeFlow()
