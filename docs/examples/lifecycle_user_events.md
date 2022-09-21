# Combining lifecycle and user events

## Upstream flows

```python
from metaflow import FlowSpec, step

class LifecycleFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Done")

if __name__ == "__main__":
    LifecycleFlow()
```

```python
from metaflow import FlowSpec, step
from metaflow.plugins import send_event

class EventFlow(FlowSpec):

    @step
    def start(self):
        send_event("ping")
        self.next(self.end)

    @step
    def end(self):
        print("Done")

if __name__ == "__main__":
    EventFlow()
```

## Downstream flow

```python
from metaflow import FlowSpec, step, trigger_on

@trigger_on(flow='LifecycleFlow', event='ping')
class TriggeredFlow(FlowSpec):

    @step
    def start(self):
        print("TriggeredFlow starting")
        self.next(self.end)

    @step
    def end(self):
        print("TriggeredFlow done")
```

## Explanation

A run of `TriggeredFlow` is starts after a run of `EventFlow` has started and emitted the `ping` event **and** a run of `LifecycleFlow` has completed.