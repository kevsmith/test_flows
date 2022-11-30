from metaflow import FlowSpec, step, trigger_on_finish, project


@trigger_on_finish(flows=["FooFlow", "BarFlow"])
@project(name="secret_squirrel")
class BazFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("BazFlow done")


if __name__ == "__main__":
    BazFlow()
