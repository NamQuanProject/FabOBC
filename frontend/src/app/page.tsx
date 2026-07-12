"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api, ApiError } from "@/lib/api";
import { DEPARTMENTS } from "@/lib/departments";
import { useSession } from "@/context/SessionContext";
import type { UserOut } from "@/lib/types";

export default function LoginPage() {
  const router = useRouter();
  const { user, hydrated, login } = useSession();
  const [users, setUsers] = useState<UserOut[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [fadingOut, setFadingOut] = useState(false);

  useEffect(() => {
    if (hydrated && user) {
      router.replace(user.role === "manager" ? "/team" : `/dept/${user.department}`);
    }
  }, [hydrated, user, router]);

  useEffect(() => {
    api
      .listUsers()
      .then(setUsers)
      .catch((err: unknown) => {
        setError(
          err instanceof ApiError
            ? `Could not reach the FabOPC API (${err.status}). Is the backend running?`
            : "Could not reach the FabOPC API. Is the backend running?"
        );
      })
      .finally(() => setLoading(false));
  }, []);

  function handleSelect(selected: UserOut) {
    setFadingOut(true);
    setTimeout(() => {
      login(selected);
      router.push(selected.role === "manager" ? "/team" : `/dept/${selected.department}`);
    }, 250);
  }

  return (
    <div className="login-root" style={{ opacity: fadingOut ? 0 : 1, transition: "opacity .25s ease" }}>
      <div className="login-bg" />
      <div className="login-wrap">
        <div className="login-side">
          <div className="brand big">
            <div className="brand-mark">F</div>
            <div className="brand-text">
              <span className="brand-name">FabOPC</span>
              <span className="brand-sub">AI Executive Team</span>
            </div>
          </div>
          <h1>
            Your embedded
            <br />
            <span className="grad-text">AI executive team.</span>
          </h1>
          <p>
            One virtual CEO orchestrating specialised agents for every department. Sign in as a
            team member to manage your work — or as the head of the company to see everything.
          </p>
          <div className="login-points">
            <div>
              <i>🤖</i> A dedicated AI agent for every faculty
            </div>
            <div>
              <i>🔐</i> Role-based access &amp; permissions
            </div>
            <div>
              <i>📊</i> Unified insight across the company
            </div>
          </div>
        </div>
        <div className="login-panel">
          <h2>Choose your account</h2>
          <p className="muted">Demo workspace · select a profile to sign in</p>
          {error && <div className="error-banner">{error}</div>}
          <div className="login-grid">
            {loading && <p className="login-empty">Loading accounts…</p>}
            {!loading && !error && users.length === 0 && (
              <p className="login-empty">
                No users found. Seed the demo workspace with{" "}
                <code>python -m scripts.seed_demo_workspace</code> in the backend.
              </p>
            )}
            {users.map((u) => {
              const dept = DEPARTMENTS[u.department];
              return (
                <button
                  key={u.id}
                  className={`login-card ${u.role}`}
                  onClick={() => handleSelect(u)}
                >
                  <div className={`login-ava ${dept.cls}`}>{u.initials}</div>
                  <div className="login-meta">
                    <strong>{u.full_name}</strong>
                    <span>{u.title}</span>
                  </div>
                  {u.role === "manager" ? (
                    <span className="login-role manager">Head of Company</span>
                  ) : (
                    <span className="login-role">{dept.short}</span>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
