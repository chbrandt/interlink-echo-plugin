"""
Minimalist interLink plugin — echoes every call to stdout and returns
the minimal valid response required by the interLink plugin API.

Run with:
    uvicorn plugin:app --host 0.0.0.0 --port 4000
"""

import json
from typing import List

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, HTMLResponse

import interlink

app = FastAPI(title="Minimalist interLink Plugin")


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def _dump(label: str, obj) -> None:
    """Pretty-print an interLink request object to stdout."""
    try:
        if isinstance(obj, list):
            data = [
                item.model_dump() if hasattr(item, "model_dump") else item
                for item in obj
            ]
        elif hasattr(obj, "model_dump"):
            data = obj.model_dump()
        else:
            data = obj
    except Exception:
        data = str(obj)
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")
    print(json.dumps(data, indent=2, default=str))
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/create")
async def create_pod(pod: interlink.Pod) -> interlink.CreateStruct:
    _dump("CREATE", pod)
    # Return a CreateStruct with the required fields
    # Note: Field names use aliases (PodUID/PodJID in JSON, pod_uid/pod_jid in Python)
    return interlink.CreateStruct(
        pod_uid=pod.pod.metadata.uid or "unknown-uid",
        pod_jid="minimalist-1",
    )


@app.post("/delete")
async def delete_pod(pod: interlink.PodRequest) -> str:
    _dump("DELETE", pod)
    return f"Pod '{pod.metadata.uid}' deleted"


@app.get("/status")
async def status_pod(pods: List[interlink.PodRequest]) -> List[interlink.PodStatus]:
    _dump("STATUS", pods)
    result = []
    for pod in pods:
        result.append(
            interlink.PodStatus(
                name=pod.metadata.name or "unknown",
                uid=pod.metadata.uid or "unknown-uid",  # Note: uid field (not UID)
                namespace=pod.metadata.namespace or "default",
                containers=[
                    interlink.ContainerStatus(
                        name=c.name,
                        state=interlink.ContainerStates(
                            waiting=interlink.StateWaiting(
                                reason="Received by minimalist plugin",
                                message="Pod handled by minimalist plugin - no actual backend"
                            ),
                        ),
                    )
                    for c in pod.spec.containers
                ],
            )
        )
    return result


@app.get("/getLogs", response_class=PlainTextResponse)
async def get_logs(req: interlink.LogRequest) -> bytes:
    _dump("GET LOGS", req)
    return b"[minimalist-plugin] no logs available\n"

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root():
    index_html = """
    <html>
        <head><title>interLink Echo Plugin</title></head>
        <body>
            <h1>Minimalist interLink Plugin</h1>
            <p>This plugin echoes all requests to stdout and returns minimal valid responses.</p>
            <p>See the <a href="/docs">docs/</a> for endpoints.</p>
        </body>
    </html>
    """
    return HTMLResponse(content=index_html, media_type="text/html")
