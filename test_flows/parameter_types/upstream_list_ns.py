from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


@project(name="koala")
class UpstreamListFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.send_lists)

    @step
    def send_lists(self):
        send_event(
            "downstream.lists",
            event_data={"my_list": ["a", "b", 1, 2, 3.45]},
            use_project=True,
        )
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    UpstreamListFlow()
