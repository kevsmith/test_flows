from metaflow import FlowSpec, trigger_on, step, project



@trigger_on(event="my-other-event")
@project(name="foobly_foo")
class BarFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Bar done")


if __name__ == "__main__":
    BarFlow()
