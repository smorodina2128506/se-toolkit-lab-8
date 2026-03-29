import httpx
import os
import json
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("mcp-obs")

VICTORIALOGS_URL = os.environ.get("NANOBOT_VICTORIALOGS_URL", "http://victorialogs:9428")
VICTORIATRACES_URL = os.environ.get("NANOBOT_VICTORIATRACES_URL", "http://victoriatraces:10428")

@mcp.tool()
def logs_search(query: str, limit: int = 20) -> str:
    """Search logs using LogsQL query."""
    with httpx.Client() as client:
        r = client.get(f"{VICTORIALOGS_URL}/select/logsql/query", params={"query": query, "limit": limit})
        return r.text

@mcp.tool()
def logs_error_count(service: str = "Learning Management Service", time_range: str = "1h") -> str:
    """Count errors per service over a time window."""
    query = f'_time:{time_range} service.name:"{service}" severity:ERROR'
    with httpx.Client() as client:
        r = client.get(f"{VICTORIALOGS_URL}/select/logsql/query", params={"query": query, "limit": 100})
        lines = [l for l in r.text.strip().split("\n") if l]
        return json.dumps({"service": service, "time_range": time_range, "error_count": len(lines)})

@mcp.tool()
def traces_list(service: str = "Learning Management Service", limit: int = 10) -> str:
    """List recent traces for a service."""
    with httpx.Client() as client:
        r = client.get(f"{VICTORIATRACES_URL}/select/jaeger/api/traces", params={"service": service, "limit": limit})
        return r.text

@mcp.tool()
def traces_get(trace_id: str) -> str:
    """Fetch a specific trace by ID."""
    with httpx.Client() as client:
        r = client.get(f"{VICTORIATRACES_URL}/select/jaeger/api/traces/{trace_id}")
        return r.text

def main():
    mcp.run()
