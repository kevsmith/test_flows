from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


class UpstreamFloatFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.send_floats)

    @step
    def send_floats(self):
        send_event("downstream.floats", event_data={"my_float": 123.456})
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    UpstreamFloatFlow()
