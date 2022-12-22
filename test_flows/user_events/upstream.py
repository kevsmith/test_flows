from metaflow import FlowSpec, step
from metaflow.plugins import send_event


class UpstreamFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.foo)

    @step
    def foo(self):
        send_event("an.event")
        self.next(self.bar)

    @step
    def bar(self):
        send_event("another.event")
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    UpstreamFlow()
