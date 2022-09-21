from metaflow import FlowSpec, step
from metaflow.plugins import send_event


class HelloFlow(FlowSpec):
    @step
    def start(self):
        send_event("woot", event_data={"person": "Wadzinski"})
        self.next(self.end)

    @step
    def end(self):
        print("Hello")


if __name__ == "__main__":
    HelloFlow()
