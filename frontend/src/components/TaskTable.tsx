import type { TaskOut } from "@/lib/types";

export function TaskTable({ tasks }: { tasks: TaskOut[] }) {
  if (tasks.length === 0) {
    return <p className="muted small">No active tasks for this department yet.</p>;
  }
  return (
    <table className="tbl">
      <thead>
        <tr>
          <th>Task</th>
          <th>Status</th>
          <th>Due</th>
        </tr>
      </thead>
      <tbody>
        {tasks.map((t) => {
          const cls = /need|escalat/i.test(t.status) ? "warn" : /done|filed/i.test(t.status) ? "ok" : "";
          return (
            <tr key={t.id}>
              <td>
                <b>{t.title}</b>
              </td>
              <td>
                <span className={`pill ${cls}`}>{t.status}</span>
              </td>
              <td className="muted">{t.due_label ?? "—"}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
