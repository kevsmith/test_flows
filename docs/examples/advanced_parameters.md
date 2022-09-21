# Advanced parameter mapping

## Upstream flows

```python
from metaflow import FlowSpec, step
from metaflow.plugins import send_event

class GivenNameFlow(FlowSpec):

    @step
    def start(self):
        send_event("my-given-name", event_data={"given_name": "Grace"})
        self.next(self.end)

    @step
    def end(self):
        print("Done")

if __name__ == "__main__":
    GivenNameFlow()
```

```python
from metaflow import FlowSpec, step
from metaflow.plugins import send_event

class SurnameFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.emit_event)

    @step
    def emit_event(self):
        send_event("my-surname", event_data={"surname": "Hopper"})
        self.next(self.end)

    @step
    def end(self):
        print("Done")

if __name__ == "__main__":
    SurnameFlow()
```
## Downstream flow

```python
from metaflow import FlowSpec, step, trigger_on
from metaflow.parameters import Parameter

@trigger_on(events=['my-surname', 'my-given-name'], 
    mappings={'my-surname': {'last_name': 'surname'}, 'my-given-name': {'first_name': 'given_name'}}                                
class FullNameFlow(FlowSpec):
    first_name = Parameter(name="first_name", required=True, type=str)
    last_name = Parameter(name="last_name", required=True, type=str)

    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print(f"My name is {self.first_name} {self.last_name}.")

if __name__ == "__main__":
    FullNameFlow()
```

## Explanation
A run of `FullNameFlow` is triggered after a run of `GivenNameFlow` emits `my-given-name` and a run of `SurnameFlow` emits `my-surname`. The mappings
declared in `FullNameFlow`'s `@trigger_on` decorator map the event fields `given_name` and `surname` to `first_name` and `last_name` respectively.
The `FullNameFlow` run prints "My name is Grace Hopper." when it finishes.