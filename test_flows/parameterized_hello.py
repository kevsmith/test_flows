from unicodedata import name
from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter


@trigger_on(event="run-me")
class ParameterizedHelloFlow(FlowSpec):

    person = Parameter(name="person", required=True, type=str)
    triggering_flow = Parameter(name="metaflow_trigger_flow_name", type=str)
    triggering_flow_spec = Parameter(name="metaflow_trigger_flow_spec", type=str)
    triggering_step_spec = Parameter(name="metaflow_trigger_step_spec")
    triggering_run = Parameter(name="metaflow_trigger_run_id", type=str)
    trigger_ts = Parameter(name="metaflow_trigger_timestamp", type=int)

    @step
    def start(self):
        print(f"Triggered by flow {self.triggering_flow}")
        print(f"Triggered by run {self.triggering_run}")
        print(f"Triggered at {self.trigger_ts}")
        print(f"Flow path spec: {self.triggering_flow_spec}")
        print(f"Step path spec: {self.triggering_step_spec}")
        self.next(self.end)

    @step
    def end(self):
        print("Hello %s" % (self.person))
        return


if __name__ == "__main__":
    ParameterizedHelloFlow()
