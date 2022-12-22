from metaflow import FlowSpec, step, trigger_on_finish, current


def assert_eq(expected, value, message=None):
    if expected != value:
        if message is None:
            raise RuntimeError(f"Expected {expected} but have {value}")
        else:
            raise RuntimeError(f"{message}\nExpected {expected} but have {value}")


@trigger_on_finish(flow="HelloFlow")
class GoodbyeFlow(FlowSpec):
    @step
    def start(self):
        if current.trigger is None:
            raise RuntimeError("current.trigger not set!")
        if current.trigger.run is None:
            raise RuntimeError("current.trigger.run not set")
        assert_eq(1, len(current.trigger), "Triggering runs")
        run = current.trigger.run
        print(f"Triggered by {run.pathspec} which started at {run.created_at}")
        self.next(self.end)

    @step
    def end(self):
        print("Goodbye")


if __name__ == "__main__":
    GoodbyeFlow()
