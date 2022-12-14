from metaflow import FlowSpec, step
from metaflow.plugins import send_event


class ShortFlow(FlowSpec):
    @step
    def start(self):
        send_event("run-me", event_data={"person": "Kevin"})
        self.next(self.end)

    @step
    def end(self):
        return


if __name__ == "__main__":
    ShortFlow()
