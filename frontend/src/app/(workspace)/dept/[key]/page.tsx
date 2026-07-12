"use client";

import { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { api, ApiError } from "@/lib/api";
import { DEPARTMENTS, DepartmentMeta } from "@/lib/departments";
import type { DepartmentDashboard, DepartmentKey } from "@/lib/types";
import { useSession } from "@/context/SessionContext";
import { KpiGrid } from "@/components/KpiGrid";
import { TaskTable } from "@/components/TaskTable";
import { ExecutiveCard } from "@/components/ExecutiveCard";

export default function DepartmentDashboardPage() {
  const { user } = useSession();
  const params = useParams<{ key: string }>();
  const router = useRouter();
  const deptKey = params.key as DepartmentKey;
  const dept: DepartmentMeta | undefined = DEPARTMENTS[deptKey];

  const [data, setData] = useState<DepartmentDashboard | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user || !dept) return;
    setLoading(true);
    setError(null);
    api
      .getDepartmentDashboard(user.company_id, deptKey)
      .then(setData)
      .catch((err: unknown) =>
        setError(err instanceof ApiError ? err.message : "Failed to load dashboard")
      )
      .finally(() => setLoading(false));
  }, [user, deptKey, dept]);

  if (!user || !dept) return null;

  const isViewingAsManager = user.role === "manager" && user.department !== deptKey;

  return (
    <div>
      {isViewingAsManager && (
        <div className="view-as">
          👁 Viewing <b>{dept.name}</b> as Head of Company
        </div>
      )}

      <div className="page-head">
        <div>
          <h1>
            <span className={`dept-dot ${dept.cls}`} />
            {dept.name}
          </h1>
          <p className="muted">
            Managed with <b>{data?.agent_persona ?? "…"}</b>, your{" "}
            {data?.agent_role_title ?? "department agent"}.
          </p>
        </div>
        <div className="head-actions">
          <button className="btn ghost" onClick={() => router.push(`/dept/${deptKey}/chat`)}>
            💬 Ask {data?.agent_persona ?? "agent"}
          </button>
          <button className="btn primary">＋ New task</button>
        </div>
      </div>

      {error && <div className="error-banner">{error}</div>}
      {loading && <p className="muted">Loading department data…</p>}

      {data && (
        <>
          <ExecutiveCard personaInitial={data.agent_persona[0] ?? "?"} tag={`${data.agent_persona.toUpperCase()} · ${data.agent_role_title}`} message={data.insight}>
            <Link href={`/dept/${deptKey}/chat`} className="chip">
              Open conversation →
            </Link>
          </ExecutiveCard>

          <KpiGrid kpis={data.kpis} />

          <div className="split wide-left">
            <div className="panel">
              <div className="panel-head">
                <h3>Active Work</h3>
                <span className="muted small">{data.tasks.length} items</span>
              </div>
              <TaskTable tasks={data.tasks} />
            </div>
            <div className="panel">
              <div className="panel-head">
                <h3>{data.agent_persona}&rsquo;s Suggestions</h3>
                <span className="nav-badge live">AI</span>
              </div>
              <div className="suggest-stack">
                {dept.suggestions.map((s) => (
                  <Link
                    key={s}
                    href={{ pathname: `/dept/${deptKey}/chat`, query: { prompt: s } }}
                    className="suggest-row"
                  >
                    {s}
                    <span>→</span>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
