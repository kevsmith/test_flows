from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


@project(name="foobly_foo")
class ThreeWayFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.foo)

    @step
    def foo(self):
        send_event("my-event")
        self.next(self.bar)

    @step
    def bar(self):
        send_event("my-other-event")
        self.next(self.end)

    @step
    def end(self):
        send_event("my-other-other-event")
        print("Done")


if __name__ == "__main__":
    ThreeWayFlow()
