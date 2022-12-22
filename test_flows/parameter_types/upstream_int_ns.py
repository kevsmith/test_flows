from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


@project(name="koala")
class UpstreamIntFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.send_ints)

    @step
    def send_ints(self):
        send_event("downstream.ints", event_data={"my_int": 123}, use_project=True)
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    UpstreamIntFlow()
