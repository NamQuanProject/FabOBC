"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { Icon } from "./Icon";
import { DEPARTMENT_ORDER, DEPARTMENTS } from "@/lib/departments";
import { useSession } from "@/context/SessionContext";

const TEAM_ICON =
  "M16 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm-8 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm0 2c-2.7 0-6 1.3-6 4v2h8v-2c0-1 .4-1.9 1-2.6A9 9 0 0 0 8 13Zm8 0c-.6 0-1.2 0-1.7.1 1 .8 1.7 1.8 1.7 2.9v2h6v-2c0-2.7-3.3-4-6-4Z";
const PROFILE_ICON = "M12 2 4 5v6c0 5 3.4 9.7 8 11 4.6-1.3 8-6 8-11V5l-8-3Z";
const LOGOUT_ICON =
  "M16 17v-2H9v-2h7V9l4 3-4 4Zm-3-12a2 2 0 0 1 2 2v2h-2V7H6v10h7v-2h2v2a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V7a2 2 0 0 1 2-2h7Z";

export function Sidebar() {
  const { user, logout } = useSession();
  const pathname = usePathname();
  const router = useRouter();

  if (!user) return null;
  const isMgr = user.role === "manager";
  const visibleDepts = isMgr ? DEPARTMENT_ORDER : [user.department];
  const selfDept = DEPARTMENTS[user.department];

  function handleLogout() {
    logout();
    router.push("/");
  }

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-mark">F</div>
        <div className="brand-text">
          <span className="brand-name">FabOPC</span>
          <span className="brand-sub">AI Executive Team</span>
        </div>
      </div>

      <nav className="nav">
        {isMgr && (
          <>
            <span className="nav-label">Command</span>
            <Link href="/team" className={`nav-item ${pathname === "/team" ? "active" : ""}`}>
              <Icon path={TEAM_ICON} />
              <span>Team Overview</span>
            </Link>
            <Link
              href="/dept/executive/chat"
              className={`nav-item ${pathname === "/dept/executive/chat" ? "active" : ""}`}
            >
              <Icon path={DEPARTMENTS.executive.icon} />
              <span>Executive Agent</span>
            </Link>
          </>
        )}

        <span className="nav-label">{isMgr ? "Departments" : "My Workspace"}</span>
        {visibleDepts.map((key) => {
          const d = DEPARTMENTS[key];
          const dashHref = `/dept/${key}`;
          const chatHref = `/dept/${key}/chat`;
          return (
            <div key={key} className="nav-dept">
              <Link href={dashHref} className={`nav-item ${pathname === dashHref ? "active" : ""}`}>
                <Icon path={d.icon} className={`ic-${d.cls}`} />
                <span>{d.name}</span>
              </Link>
              <Link href={chatHref} className={`nav-sub ${pathname === chatHref ? "active" : ""}`}>
                <i className={`dot ${d.cls}`} /> Ask agent <em className="nav-badge live">AI</em>
              </Link>
            </div>
          );
        })}

        <span className="nav-label">Company</span>
        <Link href="/profile" className={`nav-item ${pathname === "/profile" ? "active" : ""}`}>
          <Icon path={PROFILE_ICON} />
          <span>Business Profile</span>
        </Link>
      </nav>

      <div className="side-user">
        <div className={`avatar ${selfDept.cls}`}>{user.initials}</div>
        <div className="user-text">
          <strong>{user.full_name}</strong>
          <span>{user.title}</span>
        </div>
        <button className="icon-btn small" title="Sign out" onClick={handleLogout}>
          <Icon path={LOGOUT_ICON} />
        </button>
      </div>
    </aside>
  );
}
