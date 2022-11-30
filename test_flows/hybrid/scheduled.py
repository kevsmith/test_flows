from metaflow import FlowSpec, trigger_on, step, schedule


@trigger_on(event="kevsmithtest.user.kevsmith.helloflow")
@schedule(hourly=True)
class ScheduledFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Baz done")


if __name__ == "__main__":
    ScheduledFlow()
