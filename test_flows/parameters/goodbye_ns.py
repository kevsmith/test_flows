from metaflow import FlowSpec, step, trigger_on, project
from metaflow.parameters import Parameter


@project(name="donut")
@trigger_on(flow="HelloFlow")
class GoodbyeFlow(FlowSpec):
    person = Parameter(name="person", type=str)

    @step
    def start(self):
        if self.person != "Wadzinski":
            raise RuntimeError("Unexpected parameter value: %s" % self.person)
        self.next(self.end)

    @step
    def end(self):
        print(f"Goodbye {self.person}")


if __name__ == "__main__":
    GoodbyeFlow()
