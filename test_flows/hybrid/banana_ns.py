from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


@project(name="coelacanth")
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
