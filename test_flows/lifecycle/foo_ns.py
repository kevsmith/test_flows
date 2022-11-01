from metaflow import FlowSpec, step, project


@project(name="secret_squirrel")
class FooFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("FooFlow done")


if __name__ == "__main__":
    FooFlow()
