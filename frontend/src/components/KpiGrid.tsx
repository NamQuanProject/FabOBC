import type { KpiOut } from "@/lib/types";

export function KpiGrid({ kpis }: { kpis: KpiOut[] }) {
  if (kpis.length === 0) {
    return <p className="muted small">No KPIs recorded yet for this department.</p>;
  }
  return (
    <div className="kpi-grid">
      {kpis.map((k) => (
        <div className="kpi" key={k.id}>
          <div className="kpi-top">
            <span>{k.label}</span>
            {k.trend_label && <i className={`trend ${k.trend_direction ?? "flat"}`}>{k.trend_label}</i>}
          </div>
          <strong>{k.value}</strong>
        </div>
      ))}
    </div>
  );
}
