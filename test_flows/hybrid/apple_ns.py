from metaflow import FlowSpec, step, project


@project(name="coelacanth")
class AppleFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("AppleFlow done")


if __name__ == "__main__":
    AppleFlow
()
