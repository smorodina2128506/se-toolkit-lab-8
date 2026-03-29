# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

<!-- Paste the agent's response to "What is the agentic loop?" and "What labs are available in our LMS?" -->

## Task 1B — Agent with LMS tools

<!-- Paste the agent's response to "What labs are available?" and "Describe the architecture of the LMS system" -->

## Task 1C — Skill prompt

<!-- Paste the agent's response to "Show me the scores" (without specifying a lab) -->

## Task 2A — Deployed agent

Using config: /tmp/config.resolved.json
Channels enabled: webchat
MCP server 'lms': connected, 9 tools registered
MCP server 'webchat': connected, 1 tools registered
Agent loop started

## Task 2B — Web client

Flutter web client is accessible at http://10.93.26.40:42002/flutter
Agent responded to "What can you do?" with a list of capabilities including LMS integration.
Agent responded to "How is the backend doing?" with real backend data.

## Task 3A — Structured logging

### Happy path (status 200):
request_started → auth_success → db_query → request_completed
trace_id=43969d58b6aa8c4f491c2bfe1f986e8b, status 200

### Error path (postgres stopped, status 404):
request_started → auth_success → db_query (ERROR) → items_list_failed_as_not_found → request_completed
trace_id=cbfeb3598a3611967bb953f7ad79f8d3, status 404

## Task 3B — Traces

screeeeen
## Task 3C — Observability MCP tools

Healthy trace: trace_id=43969d58b6aa8c4f491c2bfe1f986e8b - spans: request_started, auth_success, db_query, request_completed
Error trace: trace_id=cbfeb3598a3611967bb953f7ad79f8d3 - error occurred at db_query step when postgres was stopped
Normal conditions: Agent reported no errors in the last 10 minutes.
Error conditions: Agent detected db_query ERROR in Learning Management Service when postgres was stopped.

## Task 4A — Multi-step investigation

Based on the traces, here's what went wrong with the LMS service:
Root Cause: DNS/Network Connectivity Issues
- Database Connection Failure: backend cannot reach PostgreSQL postgres:5432, error: socket.gaierror Name or service not known
- All queries to item table fail, causing /items/ endpoint to return 404
- Older traces show successful 200 responses, recent traces show connection timeouts of 5-13 seconds

## Task 4B — Proactive health check

LMS Health Check Results - Status: UNHEALTHY
- Backend Status: HTTP 404 error
- Recent Errors (last 2 min): 0 logged err PostgreSQL was stopped, causing /items/ endpoint to return 404

## Task 4C — Bug fix and recovery

Root cause: In backend/src/lms_backend/routers/items.py, the except Exception block 
was catching all errors and returning HTTP 404 "Items not found" instead of the real error.

Fix: Changed HTTP_404_NOT_FOUND to HTTP_503_SERVICE_UNAVAILABLE and added the real 
exception message to the response detail.

Post-fix: Agent now correctly reports "503 Service Unavailable" and "6 errors" 
with DNS resolution failure details instead of misleading 404.

Recovery: After starting postgres, system returned to healthy state.
