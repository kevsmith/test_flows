import asyncio
import json
import os

import nats

async def main(event_source, flow_name):
    conn = await nats.connect(event_source)
    msg = {"payload": {"flow_name": flow_name}}
    await conn.publish(json.dumps(msg))
    await conn.drain()

if __name__ == "__main__":
    runtime = os.getenv("METAFLOW_RUNTIME_NAME")  
    if runtime != "argo-workflows":
        raise RuntimeError(f"Unknown runtime: {runtime}")
    event_backend = os.getenv("METAFLOW_EVENT_BACKEND")
    if event_backend is None:
        raise RuntimeError("METAFLOW_EVENT_BACKEND not set")
    if event_backend != "argo-events/nats":
        raise RuntimeError(f"Unknown event backend: {event_backend}")
    event_source = os.getenv("METAFLOW_EVENT_SOURCE")
    if event_source is None:
        # Use default NATS service name
        event_source = "nats://eventbus-default-stan-svc:4222"
    elif not event_source.startswith("nats://"):
        raise RuntimeError(f"Non-NATS event source: {event_source}")
    flow_name = os.getenv("METAFLOW_FLOW_NAME")
    if flow_name is None:
        raise RuntimeError("METAFLOW_FLOW_NAME not set")
    asyncio.run(main(event_source, flow_name))