from metaflow import FlowSpec, trigger_on, step, project


@project(name="foobly_foo")
@trigger_on(event="my.other.other.event")
class QuuxFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Baz done")


if __name__ == "__main__":
    QuuxFlow()
