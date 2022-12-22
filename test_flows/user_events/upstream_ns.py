from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


@project(name="giraffe")
class UpstreamFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.foo)

    @step
    def foo(self):
        send_event("an.event", use_project=True)
        self.next(self.bar)

    @step
    def bar(self):
        send_event("another.event", use_project=True)
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    UpstreamFlow()
