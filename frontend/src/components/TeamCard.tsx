import Link from "next/link";
import type { DepartmentMeta } from "@/lib/departments";
import type { DepartmentDashboard, UserOut } from "@/lib/types";

export function TeamCard({
  user,
  dept,
  dashboard,
}: {
  user: UserOut;
  dept: DepartmentMeta;
  dashboard: DepartmentDashboard | null;
}) {
  const activeTask = dashboard?.tasks[0];
  const alert = dashboard?.tasks.some((t) => /need|escalat/i.test(t.status)) ?? false;

  return (
    <div className="team-card">
      <div className="team-top">
        <div className={`avatar ${dept.cls}`}>{user.initials}</div>
        <div>
          <strong>{user.full_name}</strong>
          <span className="muted small">{user.title}</span>
        </div>
        <span
          className={`status-dot ${alert ? "busy" : "on"}`}
          title={alert ? "Needs attention" : "On track"}
        />
      </div>
      <div className="team-dept">
        <i className={`dot ${dept.cls}`} />
        {dept.name} · agent <b>{dashboard?.agent_persona ?? "…"}</b>
      </div>
      <div className="team-now">
        <span className="muted small">Working on</span>
        <p>{activeTask ? activeTask.title : "—"}</p>
      </div>
      <div className="team-kpis">
        {(dashboard?.kpis ?? []).slice(0, 2).map((k) => (
          <div key={k.id}>
            <span>{k.label}</span>
            <b>{k.value}</b>
          </div>
        ))}
      </div>
      <div className="team-actions">
        <Link href={`/dept/${dept.key}`} className="chip">
          Dashboard
        </Link>
        <Link href={`/dept/${dept.key}/chat`} className="chip">
          Ask {dashboard?.agent_persona ?? "agent"}
        </Link>
      </div>
    </div>
  );
}
