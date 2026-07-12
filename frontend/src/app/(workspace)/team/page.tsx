"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { DEPARTMENT_ORDER, DEPARTMENTS } from "@/lib/departments";
import type { DepartmentDashboard, UserOut } from "@/lib/types";
import { useSession } from "@/context/SessionContext";
import { ExecutiveCard } from "@/components/ExecutiveCard";
import { TeamCard } from "@/components/TeamCard";

export default function TeamOverviewPage() {
  const { user } = useSession();
  const [employees, setEmployees] = useState<UserOut[]>([]);
  const [dashboards, setDashboards] = useState<Record<string, DepartmentDashboard>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;
    api
      .listUsers()
      .then(async (users) => {
        const emps = users.filter((u) => u.role === "employee");
        setEmployees(emps);
        const entries = await Promise.all(
          DEPARTMENT_ORDER.map(async (key) => {
            try {
              const dashboard = await api.getDepartmentDashboard(user.company_id, key);
              return [key, dashboard] as const;
            } catch {
              return null;
            }
          })
        );
        const map: Record<string, DepartmentDashboard> = {};
        for (const entry of entries) {
          if (entry) map[entry[0]] = entry[1];
        }
        setDashboards(map);
      })
      .finally(() => setLoading(false));
  }, [user]);

  if (!user) return null;

  const totalTasks = Object.values(dashboards).reduce((n, d) => n + d.tasks.length, 0);

  return (
    <div>
      <div className="page-head">
        <div>
          <h1>
            Good morning, {user.full_name.split(" ").slice(-1)[0]} <span className="wave">👋</span>
          </h1>
          <p className="muted">
            You oversee <b>{employees.length} team members</b> across {DEPARTMENT_ORDER.length}{" "}
            departments · {loading ? "…" : totalTasks} active tasks today.
          </p>
        </div>
        <div className="head-actions">
          <Link className="btn ghost" href="/dept/executive/chat">
            💬 Ask Orion
          </Link>
          <button className="btn primary">＋ New directive</button>
        </div>
      </div>

      <ExecutiveCard
        personaInitial="O"
        tag="ORION · Virtual CEO · Orchestrator"
        message={`Overnight I reviewed activity across ${DEPARTMENT_ORDER.length} departments. ${employees.length} agents are online.`}
      >
        <Link className="chip" href="/dept/executive/chat?prompt=Give+me+the+morning+briefing">
          📋 Morning briefing
        </Link>
        <Link className="chip" href="/dept/executive/chat?prompt=What+needs+my+approval+today%3F">
          ✔ Approvals
        </Link>
      </ExecutiveCard>

      <div className="panel-head solo">
        <h3>Your Team</h3>
        <span className="muted small">Click any member to view their dashboard or talk to their agent</span>
      </div>
      {loading ? (
        <p className="muted">Loading team overview…</p>
      ) : (
        <div className="team-grid">
          {employees.map((e) => (
            <TeamCard
              key={e.id}
              user={e}
              dept={DEPARTMENTS[e.department]}
              dashboard={dashboards[e.department] ?? null}
            />
          ))}
        </div>
      )}
    </div>
  );
}
