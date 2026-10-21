#!/usr/bin/env python3
"""Deterministic protocol peer for tests; never calls a model or reads credentials."""
import json
import sys
import time

def send(value):
    print(json.dumps(value), flush=True)

def response(request, value):
    send({"jsonrpc": "2.0", "id": request["id"], "result": value})

for raw in sys.stdin:
    request = json.loads(raw)
    method = request.get("method")
    if method == "initialize":
        response(request, {"authMethods": [{"id": "xai.api_key"}, {"id": "cached_token"}]})
    elif method == "account/read":
        response(request, {"account": {"type": "chatgpt"}})
    elif method == "authenticate":
        assert request["params"]["methodId"] == "cached_token"
        response(request, {})
    elif method == "thread/start":
        assert request["params"]["sandbox"] == "read-only"
        response(request, {"thread": {"id": "fixture-thread"}})
    elif method == "session/new":
        assert request["params"]["mcpServers"] == []
        response(request, {"sessionId": "fixture-session"})
    elif method in ("turn/start", "session/prompt"):
        params=request["params"]
        full_prompt=(params.get("input") or params.get("prompt"))[0]["text"]
        current=full_prompt.rsplit("Current user request:",1)[-1]
        if "WAIT_FOR_CANCEL" in current:
            time.sleep(120)
        reply = {"message": "Fixture explanation", "operations": []}
        if "Create a reviewable demo node" in current:
            reply = {"message": "Here is a proposed demo branch. Review it before applying.", "operations": [
                {"op": "add_node", "id": "agent-demo", "node": {"text": "Agent demo", "x": 500, "y": 1100}},
                {"op": "add_edge", "id": "agent-demo-edge", "source": "launch", "target": "agent-demo"}
            ]}
        content = json.dumps(reply)
        if method == "turn/start":
            response(request, {"turn": {"id": "fixture-turn"}})
            send({"id": "approval", "method": "item/commandExecution/requestApproval", "params": {}})
            answer = json.loads(next(sys.stdin))
            assert answer["result"]["decision"] == "decline"
            send({"method": "item/agentMessage/delta", "params": {"delta": content}})
            send({"method": "turn/completed", "params": {"turn": {"status": "completed"}}})
        else:
            send({"id": "approval", "method": "session/request_permission", "params": {}})
            answer = json.loads(next(sys.stdin))
            assert answer["result"]["outcome"]["outcome"] == "cancelled"
            send({"method": "session/update", "params": {"update": {"sessionUpdate": "agent_message_chunk", "content": {"text": content}}}})
            response(request, {"stopReason": "end_turn"})
