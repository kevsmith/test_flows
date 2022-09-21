# User events

## Upstream flow

```python
from metaflow import FlowSpec, step
from metaflow.plugins import send_event

class TwoWayFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.foo)

    @step
    def foo(self):
        send_event("my-event")
        self.next(self.bar)

    @step
    def bar(self):
        send_event("my-other-event")
        self.next(self.end)

    @step
    def end(self):
        print("Done")


if __name__ == "__main__":
    TwoWayFlow()
```

## Downstream flows

```python
from metaflow import FlowSpec, trigger_on, step

@trigger_on(event="my-event")
class BarFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Foo done")


if __name__ == "__main__":
    BarFlow()
```

```python
from metaflow import FlowSpec, trigger_on, step

@trigger_on(event="my-other-event")
class BazFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Foo done")


if __name__ == "__main__":
    BarFlow()
```

## Explanation

Running `TwoWayFlow` generates two events. `my-event` is emitted first during the `foo` step. This causes a `BarFlow` run to start. Next, `TwoWayFlow`, emits `my-other-event` during its `bar` step. This triggers a run of `BazFlow` to start. All runs execute independently of each other and as concurrently as cluster resources allow.