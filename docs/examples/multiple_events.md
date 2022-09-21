# Multiple flows

## Upstream flows

```python
from metaflow import FlowSpec, step

class FirstFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("FirstFlow done")

if __name__ == "__main__":
    FirstFlow()
```

```python
from metaflow import FlowSpec, step

class SecondFlow(FlowSpec):

    @step
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("SecondFlow done")

if __name__ == "__main__":
    SecondFlow()
```

## Downstream flow

```python
from metaflow import FlowSpec, step, trigger_on

@trigger_on(flows=['FirstFlow', 'SecondFlow'])
class ThirdFlow(FlowSpec):

    @step 
    def start(self):
        self.next(self.end)

    @step
    def end(self):
        print("ThirdFlow done")

if __name__ == "__main__":
    ThirdFlow()
```

## Explanation

A run of `ThirdFlow` is triggered after `FirstFlow` and `SecondFlow` have successful runs.