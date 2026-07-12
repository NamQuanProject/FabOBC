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

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in DATABASE_URL (Supabase), GOOGLE_API_KEY
```

Bootstrap the schema against your Supabase Postgres instance:

```bash
psql "postgresql://USER:PASSWORD@HOST:PORT/DB?sslmode=require" -f sql/init_postgresql.sql
```

Seed the demo workspace (company + 7 users matching the frontend login screen):

```bash
python -m scripts.seed_demo_workspace
```

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
