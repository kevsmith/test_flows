from metaflow import FlowSpec, step
from metaflow.plugins import send_event


class BananaFlow(FlowSpec):
    @step
    def start(self):
        send_event("banana.is.running", event_data={"score": 100})
        self.next(self.end)

    @step
    def end(self):
        print("BananaFlow done")


if __name__ == "__main__":
    BananaFlow()
