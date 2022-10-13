from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event

@project(name="coelacanth")
class BarFlow(FlowSpec):
    @step
    def start(self):
        send_event("bar.is.running", event_data={"score": 100})
        self.next(self.end)

    @step
    def end(self):
        print("BarFlow done")


if __name__ == "__main__":
    BarFlow()
