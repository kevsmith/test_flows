import asyncio
import json
import os
import sys

def call_http(url, flow_name, flow_status):
    import requests
    body = {"payload": {"flow_name": flow_name, "flow_status": flow_status}}
    resp = requests.post(url, headers={"content-type": "application/json"}, json=body)
    if resp.status_code >= 400:
        return 1
    return 0

async def call_nats(event_source, topic, flow_name, flow_status, auth_token):
    import nats
    conn = await nats.connect(event_source, token=auth_token)
    msg = {"payload": {"flow_name": flow_name, "flow_status": flow_status}}
    body = bytes(json.dumps(msg), "utf-8")
    await conn.publish(topic, body)
    await conn.drain()

def main():
    runtime = os.getenv("METAFLOW_RUNTIME_NAME")  
    if runtime != "argo-workflows":
        raise RuntimeError(f"Unknown runtime: {runtime}")
    event_source = os.getenv("METAFLOW_EVENT_SOURCE")
    if event_source is None:
        raise RuntimeError("METAFLOW_EVENT_SOURCE not set")
    if len(sys.argv) < 3:
        raise RuntimeError(f"Not enough args. Expected 3 but have {len(sys.argv)}")
    token = os.getenv("NATS_TOKEN")
    flow_name = sys.argv[1]
    flow_status = sys.argv[2].lower()

    if event_source.startswith("http://") or event_source.startswith("https://"):
        call_http(event_source, flow_name, flow_status)
    elif event_source.startswith("nats://"):
        chunks = event_source.split("/")
        topic = chunks[-1]
        nats_host = f"nats://{chunks[2]}"
        return asyncio.run(call_nats(nats_host, topic, flow_name, flow_status, token))

if __name__ == "__main__":
    sys.exit(main())
