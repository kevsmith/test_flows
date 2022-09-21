from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


@project(name="wobbly")
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
