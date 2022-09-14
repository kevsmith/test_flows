from metaflow import FlowSpec, step, annotate_lifecycle


@annotate_lifecycle(status="succeeded", data={"user": "Wadzinski"})
class HelloFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Hello")


if __name__ == "__main__":
    HelloFlow()
