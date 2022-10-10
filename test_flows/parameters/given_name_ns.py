from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event

@project(name="kipper")
class GivenNameFlow(FlowSpec):
    @step
    def start(self):
        send_event("given_name", event_data={"given_name": "Alan"})
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    GivenNameFlow()
