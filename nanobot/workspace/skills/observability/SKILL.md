# Observability Skill

Use this skill when the user asks about errors, logs, traces, or system health.

## When to use
- User asks about errors, failures, or problems
- User asks about system health or performance
- User asks to investigate a specific request or trace

## How to use

1. Start with logs_error_count to check if there are recent errors
2. Use logs_search to find specific log entries and extract trace_id
3. Use traces_get with the trace_id to inspect the full request path
4. Summarize findings concisely - do not dump raw JSON

## Example queries

- Any errors in the last hour:
  query: _time:1h service.name:"Learning Management Service" severity:ERROR

- Search for specific event:
  query: _time:10m service.name:"Learning Management Service" event:db_query

## Rules
- Always summarize, never dump raw JSON to the user
- If you find a trace_id in logs, always fetch the full trace
- Report which service failed and at which step
