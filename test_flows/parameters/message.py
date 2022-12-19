from metaflow import FlowSpec, step
from metaflow.plugins import send_event


class MessageFlow(FlowSpec):
    @step
    def start(self):
        send_event("build_message", event_data={"m": "Hola", "p": "!"})
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    MessageFlow()
