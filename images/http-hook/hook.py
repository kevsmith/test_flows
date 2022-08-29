import os
import sys

import requests

def call_hook(url, flow_name):
    body = {"payload": {"flow_name": flow_name}}
    resp = requests.post(url, headers={"content-type": "application/json"}, json=body)
    resp.raise_for_status()


def main():
    runtime = os.getenv("METAFLOW_RUNTIME_NAME")  
    if runtime != "argo-workflows":
        raise RuntimeError(f"Unknown runtime: {runtime}")
    event_backend = os.getenv("METAFLOW_EVENT_BACKEND")
    if event_backend is None:
        raise RuntimeError("METAFLOW_EVENT_BACKEND not set")
    if event_backend != "argo-events/webhook":
        raise RuntimeError(f"Unknown event backend: {event_backend}")
    event_source = os.getenv("METAFLOW_EVENT_SOURCE")
    if event_source is None:
        raise RuntimeError("METAFLOW_EVENT_SOURCE not set")
    elif (not event_source.startswith("http:") and not event_source.startswith("https:")):
        raise RuntimeError(f"Non HTTP(S) event source detected: {event_source}")
    flow_name = os.getenv("METAFLOW_FLOW_NAME")
    if flow_name is None:
        raise RuntimeError("METAFLOW_FLOW_NAME not set")
    call_hook(event_source, flow_name)

if __name__ == "__main__":
    main()
    sys.exit(0)