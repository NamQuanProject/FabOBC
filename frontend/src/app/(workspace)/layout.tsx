"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { Sidebar } from "@/components/Sidebar";
import { Topbar } from "@/components/Topbar";
import { useSession } from "@/context/SessionContext";

export default function WorkspaceLayout({ children }: { children: React.ReactNode }) {
  const { user, hydrated } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (hydrated && !user) {
      router.replace("/");
    }
  }, [hydrated, user, router]);

  if (!hydrated || !user) {
    return <div className="centered-loading">Loading workspace…</div>;
  }

  return (
    <div className="app">
      <Sidebar />
      <main className="main">
        <Topbar />
        {children}
      </main>
    </div>
  );
}
