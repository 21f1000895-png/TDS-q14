import hashlib
from fastapi import FastAPI, Request, Response

app = FastAPI()
NORMALIZED_EMAIL = "21f1000895@ds.study.iitm.ac.in"

@app.post("/")
async def mcp_endpoint(request: Request):
    try:
        body = await request.json()
    except Exception:
        body = {}

    method = body.get("method")
    req_id = body.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "exam-mcp-server", "version": "1.0.0"}
            }
        }
    elif method == "notifications/initialized":
        return Response(status_code=200)
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "solve_challenge",
                        "description": "Examines HTTP headers and solves the challenge.",
                        "inputSchema": {"type": "object", "properties": {}}
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = body.get("params", {})
        if params.get("name") == "solve_challenge":
            challenge = request.headers.get("x-exam-challenge", "")
            payload = f"{challenge}:{NORMALIZED_EMAIL}".encode("utf-8")
            full_hash = hashlib.sha256(payload).hexdigest()
            result_text = full_hash[:16]

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": result_text}]
                }
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32601, "message": "Method not found"}
    }