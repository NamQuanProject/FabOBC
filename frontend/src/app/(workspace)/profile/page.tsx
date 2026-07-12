"use client";

import { useEffect, useState } from "react";
import { api, ApiError } from "@/lib/api";
import { DEPARTMENT_ORDER, DEPARTMENTS } from "@/lib/departments";
import type { BusinessProfileOut } from "@/lib/types";
import { useSession } from "@/context/SessionContext";

const SOURCE_ICON: Record<string, string> = {
  doc: "DOC",
  spreadsheet: "XLS",
  accounting: "₫",
  crm: "CRM",
  other: "SRC",
};

export default function BusinessProfilePage() {
  const { user } = useSession();
  const [profile, setProfile] = useState<BusinessProfileOut | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;
    api
      .getBusinessProfile(user.company_id)
      .then(setProfile)
      .catch((err: unknown) =>
        setError(err instanceof ApiError ? err.message : "Failed to load business profile")
      )
      .finally(() => setLoading(false));
  }, [user]);

  if (!user) return null;

  const coverage =
    profile && profile.knowledge_sources.length > 0
      ? Math.round(
          (profile.knowledge_sources.filter((s) => s.indexed).length /
            profile.knowledge_sources.length) *
            100
        )
      : 0;

  return (
    <div>
      <div className="page-head">
        <div>
          <h1>Business Profile</h1>
          <p className="muted">The shared knowledge base every agent uses to make decisions.</p>
        </div>
        <div className="head-actions">
          <button className="btn ghost">Permissions</button>
          <button className="btn primary">Edit profile</button>
        </div>
      </div>

      {error && <div className="error-banner">{error}</div>}
      {loading && <p className="muted">Loading business profile…</p>}

      {profile && (
        <>
          <div className="profile-hero">
            <div className="profile-logo">{profile.legal_name.slice(0, 2).toUpperCase()}</div>
            <div className="profile-info">
              <h2>
                {profile.legal_name} <span className="verified">✓ Verified</span>
              </h2>
              <p className="muted">{profile.industry ?? "Industry not set"}</p>
              <div className="profile-meta">
                <span>
                  <b>Tax ID</b> {profile.tax_id ?? "—"}
                </span>
                <span>
                  <b>Employees</b> {profile.employee_count ?? "—"}
                </span>
                <span>
                  <b>Annual Rev.</b>{" "}
                  {profile.annual_revenue_vnd
                    ? `₫${(profile.annual_revenue_vnd / 1_000_000_000).toFixed(1)}B`
                    : "—"}
                </span>
                <span>
                  <b>Digital Maturity</b> Level {profile.digital_maturity_level ?? "—"}/5
                </span>
              </div>
            </div>
            <div className="maturity">
              <div
                className="maturity-ring"
                style={{ ["--p" as string]: `${((profile.digital_maturity_level ?? 0) / 5) * 100}%` }}
              >
                <span>{Math.round(((profile.digital_maturity_level ?? 0) / 5) * 100)}%</span>
              </div>
              <small className="muted">
                Decision 1567
                <br />
                readiness
              </small>
            </div>
          </div>

          <div className="split">
            <div className="panel">
              <div className="panel-head">
                <h3>Departments &amp; Agents</h3>
              </div>
              <div className="dept-list">
                {DEPARTMENT_ORDER.map((key) => {
                  const d = DEPARTMENTS[key];
                  return (
                    <div className="dept" key={key}>
                      <i className={`dot ${d.cls}`} />
                      <div>
                        <b>{d.name}</b>
                        <span className="muted small">Agent for {d.name}</span>
                      </div>
                      <span className="pill ok">Active</span>
                    </div>
                  );
                })}
              </div>
            </div>
            <div className="panel">
              <div className="panel-head">
                <h3>Company Knowledge</h3>
              </div>
              <div className="knowledge">
                {profile.knowledge_sources.length === 0 && (
                  <p className="muted small">No knowledge sources uploaded yet.</p>
                )}
                {profile.knowledge_sources.map((s) => (
                  <div className="know-item" key={s.id}>
                    <span className={`src-ic ${s.source_type}`}>
                      {SOURCE_ICON[s.source_type] ?? "SRC"}
                    </span>
                    <div>
                      <b>{s.title}</b>
                      <span className="muted small">{s.indexed ? "Indexed" : "Pending"}</span>
                    </div>
                  </div>
                ))}
                <div className="know-item add">＋ Add knowledge source</div>
              </div>
              <div className="bar-mini">
                <div className="bar-mini-label">
                  <span>Knowledge base coverage</span>
                  <b>{coverage}%</b>
                </div>
                <div className="track">
                  <div className="fill" style={{ width: `${coverage}%` }} />
                </div>
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
