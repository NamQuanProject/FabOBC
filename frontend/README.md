# FabOPC Frontend

Next.js (App Router) + TypeScript client for FabOPC. Ports the visual design
from `frontend_temp` (login → sidebar → department dashboards → per-agent
chat → team overview → business profile) into real React components backed
by the FastAPI gateway in `../backend` — no canned/static responses.

## Setup

```bash
npm install
cp .env.local.example .env.local   # points at the backend, defaults to http://127.0.0.1:8000
npm run dev                        # http://localhost:3000
```

Requires the backend running (`uvicorn app.main:app --reload` from
`../backend`) with the demo workspace seeded
(`python -m scripts.seed_demo_workspace`) so the login screen has accounts to
show. Chat replies will say a tool isn't implemented yet until the backend's
MCP tool stubs are filled in — see `../backend/README.md`.

## Structure

```text
src/app/                     App Router pages
  page.tsx                   Login (public)
  (workspace)/layout.tsx      Sidebar + Topbar shell, redirects to / if signed out
  (workspace)/team/           Manager-only team overview
  (workspace)/profile/        Business profile / knowledge base
  (workspace)/dept/[key]/     Department dashboard
  (workspace)/dept/[key]/chat/  Per-agent chat
src/components/               Sidebar, Topbar, KpiGrid, TaskTable, chat bubbles, ...
src/context/SessionContext.tsx  Client-side session (localStorage-persisted)
src/lib/api.ts                 Typed fetch client for the FastAPI gateway
src/lib/types.ts               Mirrors backend/app/schema/*.py
src/lib/departments.ts         Static per-department colors/icons/prompts
```
