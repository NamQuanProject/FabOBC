"use client";

import { DEPARTMENTS } from "@/lib/departments";
import { useSession } from "@/context/SessionContext";
import { Icon } from "./Icon";

const SEARCH_ICON = "m21 21-4.3-4.3M19 11a8 8 0 1 1-16 0 8 8 0 0 1 16 0Z";
const BELL_ICON =
  "M12 22a2.5 2.5 0 0 0 2.45-2h-4.9A2.5 2.5 0 0 0 12 22Zm6-6V11a6 6 0 0 0-5-5.9V4a1 1 0 1 0-2 0v1.1A6 6 0 0 0 6 11v5l-2 2v1h16v-1l-2-2Z";

export function Topbar() {
  const { user } = useSession();
  if (!user) return null;
  const isMgr = user.role === "manager";
  const dept = DEPARTMENTS[user.department];

  return (
    <header className="topbar">
      <div className="search">
        <Icon path={SEARCH_ICON} />
        <input type="text" placeholder="Search across your workspace…" />
        <kbd>⌘K</kbd>
      </div>
      <div className="top-actions">
        {isMgr ? (
          <span className="role-chip manager">👑 Head of Company · full access</span>
        ) : (
          <span className="role-chip">{dept.name} · team access</span>
        )}
        <button className="icon-btn" title="Notifications">
          <Icon path={BELL_ICON} />
          <span className="ping" />
        </button>
        <div className="user">
          <div className={`avatar ${dept.cls}`}>{user.initials}</div>
          <div className="user-text">
            <strong>{user.full_name}</strong>
            <span>{user.title}</span>
          </div>
        </div>
      </div>
    </header>
  );
}
