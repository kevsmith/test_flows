from metaflow import FlowSpec, step
from metaflow.plugins import send_event


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
