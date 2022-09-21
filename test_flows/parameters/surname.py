from metaflow import FlowSpec, step
from metaflow.plugins import send_event


class SurnameFlow(FlowSpec):
    @step
    def start(self):
        send_event("surname", event_data={"surname": "Turing"})
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    SurnameFlow()
