import json
from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


@project(name="koala")
class UpstreamJsonFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.send_dicts)

    @step
    def send_dicts(self):
        data = json.dumps(
            {"a": "b", "c": 123, "d": {"a": 456.789, "b": [1, 2, 3, "four"]}}
        )
        send_event(
            "downstream.json",
            event_data={"my_json": data},
            use_project=True,
        )
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    UpstreamJsonFlow()
