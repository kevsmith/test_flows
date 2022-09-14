from metaflow import FlowSpec, step, trigger_on, project
from metaflow.parameters import Parameter


@project(name="wobbly")
@trigger_on(event="run-me")
class ParametersFlow(FlowSpec):

    person = Parameter(name="person", required=True, type=str)

    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        if self.person != "Kevin":
            raise RuntimeError(
                "Expected person to be 'Kevin' but have '%s'" % self.person
            )
        print("Hello %s" % (self.person))
        return


if __name__ == "__main__":
    ParametersFlow()
