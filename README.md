# FabOPC — Operations Performance Commander

A private, on-premise multi-agent AI management layer for Vietnamese SMEs. An
Orchestrator agent ("Orion", acting as a virtual CEO) routes to six
specialized department agents — Finance, Marketing, Operations, HR,
Compliance, and Business Intelligence — all sharing a common **OPC Profile
Object**: a structured, auditable business-context state that lets one
agent's findings (e.g. Finance flags tightening cash flow) become instantly
visible to every other agent, without re-entering data.

See `proposal/` for the full submission (problem statement, architecture
innovations, business model, market sizing, roadmap).

## Repository Layout

```text
backend/           FastAPI gateway + 7 Google ADK agents + MCP tool servers (see backend/README.md)
frontend/          Next.js + TypeScript client (see frontend/README.md)
proposal/          Original competition submission (PDF report + video)
frontend_temp/     Static HTML/CSS/JS design reference the real frontend was built from
InsightForge_temp/ Earlier project used as an architectural reference (A2A server-per-agent + MCP pattern)
```

## Architecture at a Glance

```text
┌─────────────┐      REST       ┌──────────────────┐
│  Next.js UI │ ───────────────▶│  FastAPI gateway  │
└─────────────┘                 │   (backend/app)   │
                                 └─────────┬─────────┘
                                           │ A2A
                     ┌─────────────────────┼─────────────────────┐
                     ▼                     ▼                     ▼
              ┌─────────────┐      ┌──────────────┐      ┌──────────────┐
              │ Orion       │◀────▶│ Atlas / Nova │ ...  │ Lex / Echo   │
              │ Orchestrator│ A2A  │ dept. agents │      │ dept. agents │
              └──────┬──────┘      └──────┬───────┘      └──────┬───────┘
                     │ MCP                │ MCP                 │ MCP
                     ▼                    ▼                     ▼
          orchestration_servers   finance/marketing/...   compliance/bi servers
                     │                    │                     │
                     └────────────────────┴─────────────────────┘
                                           │
                              Supabase REST API
                        (OPC Profile Object, users, KPIs, chat)
```

- **Agents**: each department agent (Atlas/Finance, Nova/Marketing,
  Forge/Operations, Sage/HR, Lex/Compliance, Echo/BI) is a Google ADK
  `LlmAgent` on Gemini, served as its own A2A process. Orion, the
  orchestrator, hands off to them via A2A and synthesizes their answers.
- **Tools**: each agent's capabilities are exposed through its own MCP tool
  server (`backend/mcp_servers/`). Tool bodies are currently structured
  stubs — signatures, types, and docstrings are real; the business logic
  isn't implemented yet (see `backend/mcp_servers/shared/stub.py`).
- **Shared state**: the OPC Profile Object (`backend/core/opc_profile.py`)
  is persisted as JSONB in Supabase. The backend has no self-hosted database
  and never opens a direct Postgres connection — it reaches Supabase over
  its REST API (`backend/database/client.py`), the same as you'd use the
  Supabase client for storage or auth. Tables/sample data are managed
  directly in the Supabase SQL Editor, not via backend migrations.
- **Frontend**: a fully working Next.js app (login, department dashboards,
  team overview, business profile, per-agent chat) — no canned data, every
  screen calls the FastAPI gateway.

## Quickstart

There's no self-hosted database and the backend never opens a direct
Postgres connection — it talks to Supabase over its REST API, and you
manage tables/data yourself in the Supabase SQL Editor.

**Test the UI first, no agents needed:**

1. In your Supabase project's **SQL Editor**, run `backend/sql/init_postgresql.sql`
   then `backend/sql/seed_sample_data.sql` (sample company/users/KPIs/tasks).
2. From `backend/`:

   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env   # fill in SUPABASE_URL/SUPABASE_KEY (service_role) from your project
   uvicorn app.main:app --reload   # http://127.0.0.1:8000/docs
   ```

Then (from `frontend/`):

```bash
npm install
cp .env.local.example .env.local   # defaults to http://127.0.0.1:8000
npm run dev                        # http://localhost:3000
```

You can now log in and click through dashboards, team overview, and business
profile with real seeded data. Chat will reply that its agent isn't
implemented yet until you also start the agent processes:

```bash
# in separate terminals, from backend/ (orchestrator last):
python -m agents.finance_agent.main
python -m agents.marketing_agent.main
python -m agents.operations_agent.main
python -m agents.hr_agent.main
python -m agents.compliance_agent.main
python -m agents.bi_agent.main
python -m agents.orchestrator_agent.main
```

Full details, environment variables, and troubleshooting are in
[`backend/README.md`](backend/README.md) and
[`frontend/README.md`](frontend/README.md).

## Status

Structural scaffold, not a finished product:

- ✅ Frontend is fully implemented and wired to real API calls.
- ✅ Routing/orchestration plumbing (FastAPI ⇄ A2A ⇄ agents ⇄ MCP) is real
  and verified to import/build cleanly.
- ✅ The Supabase data layer is verified end-to-end against a live project
  (FastAPI ⇄ Supabase REST) — the only thing standing between you and a
  working login/dashboard is running the two SQL scripts once.
- ⏳ MCP tool bodies (the actual business logic — VAT calculation, churn
  detection, inventory health, etc.) are typed stubs. Implement one by
  replacing its `raise not_implemented(...)` line; the signature doesn't
  change.
