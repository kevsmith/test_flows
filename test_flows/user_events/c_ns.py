from metaflow import FlowSpec, trigger_on, step, project


@trigger_on(event="my-other-other-event")
@project(name="foobly_foo")
class CFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("C done")


if __name__ == "__main__":
    CFlow()
