#!/usr/bin/env python3
"""Save a Figma frame screenshot via the Figma MCP server.

Usage:
    python3 scripts/save_screenshot.py <node_id> <output_path>

Example:
    python3 scripts/save_screenshot.py 1797:83093 reports/2026-03-18-1015-my-frame.png
"""

import sys
import os
import json
import base64
import http.client

MCP_HOST = "127.0.0.1"
MCP_PORT = 3845


def main():
    if len(sys.argv) != 3:
        print(__doc__.strip())
        sys.exit(1)

    node_id = sys.argv[1]
    output_path = sys.argv[2]

    conn = http.client.HTTPConnection(MCP_HOST, MCP_PORT)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    }

    # Initialize MCP session
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-03-26",
            "capabilities": {},
            "clientInfo": {"name": "figmabuddy-cli", "version": "1.0.0"},
        },
    })
    conn.request("POST", "/mcp", body, headers)
    resp = conn.getresponse()
    session_id = resp.getheader("mcp-session-id")
    resp.read()

    if not session_id:
        print("Error: Could not obtain MCP session ID. Is the Figma MCP server running?")
        sys.exit(1)

    headers["mcp-session-id"] = session_id

    # Send initialized notification
    body = json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"})
    conn.request("POST", "/mcp", body, headers)
    conn.getresponse().read()

    # Request screenshot
    body = json.dumps({
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {
            "name": "get_screenshot",
            "arguments": {"nodeId": node_id},
        },
    })
    conn.request("POST", "/mcp", body, headers)
    resp = conn.getresponse()
    raw = resp.read().decode()

    # Parse SSE or plain JSON
    if raw.startswith("event:"):
        data_lines = [line[6:] for line in raw.split("\n") if line.startswith("data: ")]
        if data_lines:
            raw = data_lines[0]

    parsed = json.loads(raw)

    for item in parsed.get("result", {}).get("content", []):
        if item.get("type") == "image":
            img_data = base64.b64decode(item["data"])
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(img_data)
            print(f"Saved {len(img_data)} bytes → {output_path}")
            break
    else:
        print("Error: No image found in MCP response.")
        print(raw[:500])
        sys.exit(1)

    conn.close()


if __name__ == "__main__":
    main()
