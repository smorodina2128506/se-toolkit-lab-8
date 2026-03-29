#!/usr/bin/env python3
"""Entrypoint for nanobot gateway in Docker."""
import json
import os
import sys

def main():
    config_path = "/app/nanobot/config.json"
    resolved_path = "/tmp/config.resolved.json"
    workspace_path = "/app/nanobot/workspace"
    
    with open(config_path, "r") as f:
        config = json.load(f)
    
    if os.environ.get("LLM_API_KEY"):
        config.setdefault("providers", {}).setdefault("custom", {})["apiKey"] = os.environ["LLM_API_KEY"]
    if os.environ.get("LLM_API_BASE_URL"):
        config.setdefault("providers", {}).setdefault("custom", {})["apiBase"] = os.environ["LLM_API_BASE_URL"]
    if os.environ.get("LLM_API_MODEL"):
        config.setdefault("agents", {}).setdefault("defaults", {})["model"] = os.environ["LLM_API_MODEL"]
    if os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS"):
        config.setdefault("gateway", {})["host"] = os.environ["NANOBOT_GATEWAY_CONTAINER_ADDRESS"]
    if os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT"):
        config.setdefault("gateway", {})["port"] = int(os.environ["NANOBOT_GATEWAY_CONTAINER_PORT"])
    lms_backend_url = os.environ.get("NANOBOT_LMS_BACKEND_URL")
    lms_api_key = os.environ.get("NANOBOT_LMS_API_KEY")
    if lms_backend_url or lms_api_key:
        config.setdefault("tools", {}).setdefault("mcpServers", {}).setdefault("lms", {}).setdefault("env", {})
        if lms_backend_url:
            config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_BACKEND_URL"] = lms_backend_url
        if lms_api_key:
            config["tools"]["mcpServers"]["lms"]["env"]["NANOBOT_LMS_API_KEY"] = lms_api_key
    webchat_host = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS")
    webchat_port = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT")
    access_key = os.environ.get("NANOBOT_ACCESS_KEY")
    if webchat_host or webchat_port:
        config.setdefault("channels", {}).setdefault("webchat", {})["enabled"] = True
        config["channels"]["webchat"]["allowFrom"] = ["*"]
        if webchat_host:
            config["channels"]["webchat"]["host"] = webchat_host
        if webchat_port:
            config["channels"]["webchat"]["port"] = int(webchat_port)
        if access_key:
            config["channels"]["webchat"]["accessKey"] = access_key
    config.setdefault("tools", {}).setdefault("mcpServers", {})["webchat"] = {
        "command": "python",
        "args": ["-m", "mcp_webchat"],
        "env": {
            "WEBCHAT_URL": f"http://localhost:{webchat_port or 18791}",
            "WEBCHAT_ACCESS_KEY": access_key or ""
        }
    }
    config["tools"]["mcpServers"]["obs"] = {
        "command": "python",
        "args": ["-m", "mcp_obs"],
        "env": {
            "NANOBOT_VICTORIALOGS_URL": os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428"),
            "NANOBOT_VICTORIATRACES_URL": os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")
        }
    }
    with open(resolved_path, "w") as f:
        json.dump(config, f, indent=2)
    print(f"Using config: {resolved_path}", file=sys.stderr)
    os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_path, "--workspace", workspace_path])

if __name__ == "__main__":
    main()
