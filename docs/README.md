## API

### @trigger_on

Flows declare dependencies on other flows and user events via the `@trigger_on` flow decorator. This triggers dependent flows when the upstream flow succeeds.

```python
from metaflow import FlowSpec, step, trigger_on

@trigger_on(flow='MyUpstreamFlow')
class MyDownstreamFlow(FlowSpec):
```

```python
from metaflow import FlowSpec, step, trigger_on

@trigger_on(event='my-custom-event')
class MyFlow(FlowSpec):
```

`@trigger_on` can also express dependencies on multiple flows and/or events. This will trigger the dependent flow when **all** flows and events have succeeded.

```python
from metaflow import FlowSpec, step, trigger_on

@trigger_on(flows=['MyFirstUpstreamFlow', 'MySecondUpstreamFlow'])
class MyDownstreamFlow(FlowSpec):
```
```python
from metaflow import FlowSpec, step, trigger_on

@trigger_on(flow='MyUpstreamFlow', event='my-custom-event')
class MyDownstreamFlow(FlowSpec):
```

```python
from metaflow import FlowSpec, step, trigger_on

@trigger_on(flows=['MyUpstreamFlow', 'MyNightlyFlow'], events=['my-custom-event1', 'my-custom-event2'])
class MyAwesomeFlow(FlowSpec):
```

### send_event()

Flows can emit custom events via `send_event()`. Event names can contain only lowercase alphanumeric characters and '-'.

```python
from metaflow import FlowSpec, step, trigger_on
from metaflow.plugins import send_event

class UpstreamFlow(FlowSpec):

    @step
    def start(self):
        send_event(f"{self.__class__.__name__.lower()}-starting")
        self.next(self.end)
```

Custom events can contain arbitrary data so long as it's JSON serializable.

```python
from metaflow import FlowSpec, step, trigger_on
from metaflow.plugins import send_event

class UpstreamFlow(FlowSpec):
.
.
.
    @step
    def do_stuff(self):
        send_event("more-data", event_data={"extra-data": self.data})
```

Custom event data are automatically mapped to flow parameters, if any exist. Flows receiving custom events can also use `@trigger_on`'s `mappings` attribute
to rename event data fields to match parameters. See [this](./basic_parameters.md) link for a detailed example.

## Examples

See the links below for annotated examples.

[Basic lifecycle](./examples/basic_lifecycle.md)

[User generated event](./examples/user_event.md)

[Basic parameter mapping](./examples/basic_parameters.md)

[Multiple flows/events](./examples/multiple_events.md)

[Combining lifecycle and user events](./examples/lifecycle_user_events.md)

[Advanced parameter mapping](./examples/advanced_parameters.md)