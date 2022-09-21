from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter


@trigger_on(
    events=["given_name", "surname"],
    mappings={
        "given_name": {"first_name": "given_name"},
        "surname": {"last_name": "surname"},
    },
)
class FullNameFlow(FlowSpec):

    first_name = Parameter(name="first_name", required=True, type=str)
    last_name = Parameter(name="last_name", required=True, type=str)

    @step
    def start(self):
        if self.first_name != "Alan":
            raise RuntimeError("Unexpected first name: %s" % self.first_name)
        if self.last_name != "Turing":
            raise RuntimeError("Unexpected last name: %s" % self.last_name)
        self.next(self.end)

    @step
    def end(self):
        print("Name: %s %s" % (self.first_name, self.last_name))


if __name__ == "__main__":
    FullNameFlow()
