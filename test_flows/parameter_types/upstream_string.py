from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


class UpstreamStringFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.send_strings)

    @step
    def send_strings(self):
        send_event("downstream.strings", event_data={"my_string": "abc"})
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    UpstreamStringFlow()
