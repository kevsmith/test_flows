from metaflow import FlowSpec, step, emit_event


def extra_data(cls):
    return dict(person="Kevin")


class ShortFlow(FlowSpec):
    @emit_event(event="run-me", data={"person": "Kevin"})
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        return


if __name__ == "__main__":
    ShortFlow()
