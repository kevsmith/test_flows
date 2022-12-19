from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


@project(name="koala")
class UpstreamDictFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.send_dicts)

    @step
    def send_dicts(self):
        send_event(
            "downstream.dicts",
            event_data={"my_dict": {"a": "b", "c": 123, "d": {"a": 456.789}}},
        )
        send_event(
            "downstream.dicts",
            event_data={"my_dict": {"a": "b", "c": 123, "d": {"a": 456.789}}},
            use_project=True,
        )
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    UpstreamDictFlow()
