# Basic Lifecycle

## Upstream flow

```python
from metaflow import FlowSpec, step

class HelloFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Hello")


if __name__ == "__main__":
    HelloFlow()
```

## Downstream flow

```python
from metaflow import FlowSpec, step, trigger_on

@trigger_on(flow="HelloFlow")
class GoodbyeFlow(FlowSpec):
    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("Goodbye")


if __name__ == "__main__":
    GoodbyeFlow()
```

## Explanation

`GoodbyeFlow` will be triggered whenever a run of `HelloFlow` succeeds.