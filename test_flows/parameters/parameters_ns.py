from metaflow import FlowSpec, step, trigger_on, project, current
from metaflow.parameters import Parameter


def assert_eq(expected, value, message=None):
    if expected != value:
        if message is None:
            raise RuntimeError(f"Expected {expected} but have {value}")
        else:
            raise RuntimeError(f"{message}\nExpected {expected} but have {value}")


@trigger_on(events=["run-me"])
@project(name="wobbly")
class ParametersFlow(FlowSpec):

    person = Parameter(name="person", required=True, type=str)

    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        assert_eq(1, len(current.trigger), "Triggering events")
        if self.person != "Kevin":
            raise RuntimeError(
                "Expected person to be 'Kevin' but have '%s'" % self.person
            )
        print("Hello %s" % (self.person))
        return


if __name__ == "__main__":
    ParametersFlow()
