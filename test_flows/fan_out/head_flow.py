from metaflow import FlowSpec, step


class HeadFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("HeadFlow done")


if __name__ == "__main__":
    HeadFlow()
