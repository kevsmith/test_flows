from metaflow import FlowSpec, step, trigger_on_finish, current


def assert_eq(expected, value, message=None):
    if expected != value:
        if message is None:
            raise RuntimeError(f"Expected {expected} but have {value}")
        else:
            raise RuntimeError(f"{message}\nExpected {expected} but have {value}")


@trigger_on_finish(flows=["HelloFlow"])
class FarewellFlow(FlowSpec):
    @step
    def start(self):
        assert_eq(1, len(current.trigger), "Triggering runs")
        self.next(self.end)

    @step
    def end(self):
        print("Fare thee well")


if __name__ == "__main__":
    FarewellFlow()
