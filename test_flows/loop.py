from metaflow import FlowSpec, step, emit_event


class LoopFlow(FlowSpec):
    def __init__(self):
        super().__init__()

    @step
    def start(self):
        self.values = range(0, 10)
        self.total = 0
        self.next(self.per_value, foreach="values")

    @emit_event(event="")
    @step
    def per_value(self):
        import random

        self.updated_value = self.input + random.randint(5, 20)
        self.next(self.join)

    @step
    def join(self, inputs):
        self.total = sum(inputs)
        self.next(self.end)

    @step
    def end(self):
        print("Total: %d" % self.total)


if __name__ == "__main__":
    LoopFlow()
