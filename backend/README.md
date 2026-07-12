# FabOPC Backend

FastAPI gateway + a multi-agent AI executive team for FabOPC, Vietnamese SMEs'
private, on-premise multi-agent management layer (see `/proposal`). Architecture
pattern is adapted from `InsightForge_temp`: one **A2A server process per agent**,
each with its own **MCP tool server**, fronted by a FastAPI gateway — but built on
**Google ADK + Gemini** (per the proposal's stated architecture) instead of
`beeai_framework`.

There is no self-hosted database and the backend never opens a direct
Postgres connection — all relational data (users, OPC profiles, KPIs, tasks,
chat) is read/written through **Supabase's REST API** (`database/client.py`),
the same way you'd use the Supabase client for storage or auth. You manage
the actual Postgres tables yourself in the Supabase SQL Editor / Table
Editor — the backend only ever talks HTTPS to Supabase, never raw Postgres.

**Status:** structural scaffold. Routing, persistence, and the A2A/MCP plumbing
are real; every MCP tool body is a typed stub that raises `NotImplementedTool`
(see `mcp_servers/shared/stub.py`) describing what it should do. Implement a
tool by replacing its `raise not_implemented(...)` line — signatures don't change.

## Project Shape

```text
app/            FastAPI routes, schemas, services (the gateway)
core/           OPC Profile Object, agent registry/ports, personas, settings
agents/         One Google ADK LlmAgent + A2A server per agent (orchestrator + 6 depts)
mcp_servers/    One MCP tool server per agent domain (stub tool bodies)
database/       Async Supabase client — the backend's only data access path
sql/            Schema + sample data, run directly in the Supabase SQL Editor
```

The seven agents: **Orion** (Orchestrator/CEO), **Atlas** (Finance), **Nova**
(Marketing), **Forge** (Operations), **Sage** (HR), **Lex** (Compliance), **Echo**
(Business Intelligence).

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` from your Supabase project (Project Settings -> API):

```env
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_KEY=<service-role-secret-key>
```

Use the **service_role** secret, not the anon/publishable key — the backend
is a trusted server context and should read/write freely regardless of any
Row Level Security policies you add later. (If you only have the anon key
handy, it'll still work today since the schema below ships with RLS off —
just don't rely on that for anything beyond local dev.)

### Create the schema and sample data

You manage the database yourself in the Supabase dashboard — the backend
never runs DDL. Open the **SQL Editor** for your project and run, in order:

1. `sql/init_postgresql.sql` — creates the tables.
2. `sql/seed_sample_data.sql` — one demo company, its 7 users, and
   KPIs/tasks/knowledge sources for every department: everything the
   frontend needs to render fully without any agent process running.
   Idempotent — re-run any time to reset the demo data.

At this point `uvicorn app.main:app --reload` + the frontend (`../frontend`)
is enough to click through login, dashboards, team overview, and business
profile with real data — chat will reply that its agent isn't implemented
yet until you also start the agent processes below.

## Running

All commands run from this `backend/` directory so `app`, `core`, `agents`,
`mcp_servers`, and `database` resolve as top-level packages.

```bash
# Gateway
uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs

# Agents (each is its own A2A server; MCP tool servers are spawned as stdio
# subprocesses automatically by each agent's MCPToolset)
python -m agents.finance_agent.main
python -m agents.marketing_agent.main
python -m agents.operations_agent.main
python -m agents.hr_agent.main
python -m agents.compliance_agent.main
python -m agents.bi_agent.main
python -m agents.orchestrator_agent.main   # start last: hands off to the six above
```

`GET /api/v1/agents/status` reports which agent A2A servers are reachable.

## Notes

- Every tool body under `mcp_servers/` is a stub — see the module docstrings
  for the intended data source and logic per the FabOPC proposal.
- `core/opc_profile.py` is the OPC Profile Object (proposal Innovation 1): the
  shared, Pydantic-validated business context every agent reads/writes.
- Restart an agent process after editing its persona/instruction or its MCP
  server's tool set.
