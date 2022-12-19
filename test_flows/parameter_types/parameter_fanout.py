from metaflow import FlowSpec, step, project
from metaflow.plugins import send_event


@project(name="koala")
class UpstreamStringFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.send_strings)

    @step
    def send_strings(self):
        send_event("downstream.strings", data={"my_string": "abc"})
        send_event("downstream.strings", data={"my_string": "abc"}, use_project=True)
        self.next(self.send_ints)

    @step
    def send_ints(self):
        send_event("downstream.ints", data={"my_int": 123})
        send_event("downstream.ints", data={"my_int": 123}, use_project=True)
        self.next(self.send_floats)

    @step
    def send_floats(self):
        send_event("downstream.floats", data={"my_int": 123.456})
        send_event("downstream.floats", data={"my_int": 123.456}, use_project=True)
        # self.next(self.send_lists)
        self.next(self.end)

    # @step
    # def send_lists(self):
    #     send_event("downstream.lists", data={"my_list": ["a", "b", 1, 2, 3.45]})
    #     send_event(
    #         "downstream.lists",
    #         data={"my_list": ["a", "b", 1, 2, 3.45]},
    #         use_project=True,
    #     )
    #     self.next(self.send_dicts)

    # @step
    # def send_dicts(self):
    #     send_event(
    #         "downstream.dicts",
    #         data={"my_dict": {"a": "b", "c": 123, "d": {"a": 456.789}}},
    #     )
    #     send_event(
    #         "downstream.dicts",
    #         data={"my_dict": {"a": "b", "c": 123, "d": {"a": 456.789}}},
    #         use_project=True,
    #     )
    #     self.next(self.end)

    @step
    def end(self):
        print("Done")
