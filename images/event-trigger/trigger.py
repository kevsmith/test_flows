import asyncio
from datetime import datetime
import json
import os
import sys


def call_http(url, body):
    import requests

    resp = requests.post(url, headers={"content-type": "application/json"}, json=body)
    if resp.status_code >= 400:
        return 1
    return 0


async def call_nats(event_source, msg, auth_token):
    import nats

    chunks = event_source.split("/")
    topic = chunks[-1]
    nats_host = f"nats://{chunks[2]}"
    conn = await nats.connect(event_source, token=auth_token)
    body = bytes(json.dumps(msg), "utf-8")
    await conn.publish(topic, body)
    await conn.drain()


def make_payload(flow_name, flow_status, data):
    ts = int(datetime.utcnow().timestamp())
    data["metaflow_trigger_timestamp"] = ts
    # Emitting raw event
    if flow_name == "event":
        msg = {"payload": {"event_name": flow_status, "data": data, "timestamp": ts}}
    else:
        msg = {
            "payload": {
                "flow_name": flow_name,
                "flow_status": flow_status.lower(),
                "data": data,
                "timestamp": ts,
            }
        }
    return msg


def main():
    runtime = os.getenv("METAFLOW_RUNTIME_NAME")
    if runtime != "argo-workflows":
        raise RuntimeError(f"Unknown runtime: {runtime}")
    event_source = os.getenv("METAFLOW_EVENT_SOURCE")
    if event_source is None:
        raise RuntimeError("METAFLOW_EVENT_SOURCE not set")
    if len(sys.argv) < 3:
        raise RuntimeError(
            f"Not enough args. Expected at least 3 but have {len(sys.argv)}"
        )
    if len(sys.argv) == 4:
        data = json.loads(sys.argv[3])
    else:
        data = {}
    flow_path_spec = "%s/%s" % (
        os.getenv("METAFLOW_FLOW_NAME"),
        os.getenv("METAFLOW_RUN_ID"),
    )
    step_path_spec = "%s/%s" % (flow_path_spec, os.getenv("METAFLOW_STEP_NAME"))
    data["metaflow_trigger_flow_spec"] = flow_path_spec
    data["metaflow_trigger_step_spec"] = step_path_spec
    data["metaflow_trigger_flow_name"] = os.getenv("METAFLOW_FLOW_NAME")
    data["metaflow_trigger_run_id"] = os.getenv("METAFLOW_RUN_ID")
    token = os.getenv("NATS_TOKEN")
    payload = make_payload(sys.argv[1], sys.argv[2], data)

    if event_source.startswith("http://") or event_source.startswith("https://"):
        call_http(event_source, payload)
    elif event_source.startswith("nats://"):
        return asyncio.run(call_nats(event_source, payload, token))


if __name__ == "__main__":
    sys.exit(main())
