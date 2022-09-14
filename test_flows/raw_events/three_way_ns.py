from metaflow import FlowSpec, emit_event, step, project


@project(name="foobly_foo")
class ThreeWayFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.foo)

    @emit_event(event="my-event")
    @step
    def foo(self):
        self.next(self.bar)

    @emit_event(event="my-other-event")
    @step
    def bar(self):
        self.next(self.end)

    @emit_event(event="my-other-other-event")
    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    ThreeWayFlow()
