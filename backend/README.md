# FabOPC Backend

FastAPI gateway + a multi-agent AI executive team for FabOPC, Vietnamese SMEs'
private, on-premise multi-agent management layer (see `/proposal`). Architecture
pattern is adapted from `InsightForge_temp`: one **A2A server process per agent**,
each with its own **MCP tool server**, fronted by a FastAPI gateway — but built on
**Google ADK + Gemini** (per the proposal's stated architecture) instead of
`beeai_framework`.

**Status:** structural scaffold. Routing, persistence, and the A2A/MCP plumbing
are real; every MCP tool body is a typed stub that raises `NotImplementedTool`
(see `mcp_servers/shared/stub.py`) describing what it should do. Implement a
tool by replacing its `raise not_implemented(...)` line — signatures don't change.

## Project Shape

```text
app/            FastAPI routes, schemas, services, DB bootstrap (the gateway)
core/           OPC Profile Object, agent registry/ports, personas, settings
agents/         One Google ADK LlmAgent + A2A server per agent (orchestrator + 6 depts)
mcp_servers/    One MCP tool server per agent domain (stub tool bodies)
database/       Supabase client helper
sql/            Postgres schema bootstrap
scripts/        Demo data seeding
```

The seven agents: **Orion** (Orchestrator/CEO), **Atlas** (Finance), **Nova**
(Marketing), **Forge** (Operations), **Sage** (HR), **Lex** (Compliance), **Echo**
(Business Intelligence).

## Setup

There is no self-hosted database — Supabase's own Postgres instance is
the database. Nothing else to stand up locally.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` from your Supabase project (Project Settings -> Database for
`DATABASE_URL`, Project Settings -> API for `SUPABASE_URL`/`SUPABASE_KEY`):

```env
DATABASE_URL=postgresql+asyncpg://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres
SUPABASE_URL=https://<project-ref>.supabase.co
SUPABASE_KEY=<anon-or-publishable-key>
```

If the direct `db.<project-ref>.supabase.co` host doesn't connect from your
network (it's IPv6; some networks can't reach it), copy the **Session
pooler** connection string from that same Database settings page instead —
it's IPv4 and drops in as `DATABASE_URL` unchanged.

Create the schema, either by starting the app once (`app.db.init_db()` runs
`create_all` on startup) or directly:

```bash
psql "$DATABASE_URL" -f sql/init_postgresql.sql
# or paste sql/init_postgresql.sql into the Supabase SQL Editor
```

### Sample data (test the UI before touching agents)

`sql/seed_sample_data.sql` populates one demo company, its 7 users, and
KPIs/tasks/knowledge sources for every department — everything the frontend
needs to render fully without any agent process running. Run it the same way:

```bash
psql "$DATABASE_URL" -f sql/seed_sample_data.sql
# or paste it into the Supabase SQL Editor
```

It's idempotent (deletes and re-inserts the demo company each time), so
re-run it any time you want to reset the demo data. At this point
`uvicorn app.main:app --reload` + the frontend (`../frontend`) is enough to
click through login, dashboards, team overview, and business profile with
real data — chat will reply that its agent isn't implemented yet until you
also start the agent processes below.

`scripts/seed_demo_workspace.py` is a Python-side equivalent that only seeds
the company + users (no KPIs/tasks) — useful if you want to seed
programmatically rather than via SQL.

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
