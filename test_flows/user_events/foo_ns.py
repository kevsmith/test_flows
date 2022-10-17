from metaflow import FlowSpec, trigger_on, step, project


@project(name="foobly_foo")
@trigger_on(event="my-event")
class FooFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Foo done")


if __name__ == "__main__":
    FooFlow()
