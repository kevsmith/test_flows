# Basic parameter mapping

## Upstream flow

```python
from metaflow import FlowSpec, step
from metaflow.plugins import send_event

class MyNameFlow(FlowSpec):
    @step
    def start(self):
        send_event("run-me", event_data={"name": "Kevin"})
        self.next(self.end)

    @step
    def end(self):
        return


if __name__ == "__main__":
    MyNameFlow()
```

## Downstream flow

```python
from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter

@trigger_on(event="run-me")
class SayMyNameFlow(FlowSpec):

    name = Parameter(name="name", required=True, type=str)

    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print(f"My name is {name}.")


if __name__ == "__main__":
    SayMyNameFlow()
```

## Explanation

Running `MyNameFlow` emits the custom event `run-me` with a dict payload. A run of `SayMyNameFlow` is triggered by `run-me` and automatically maps the event payload `name` field
to its `name` parameter. The run prints "My name is Kevin." when it finishes.