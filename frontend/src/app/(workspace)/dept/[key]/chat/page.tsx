"use client";

import { Suspense, useEffect, useRef, useState } from "react";
import { useParams, useRouter, useSearchParams } from "next/navigation";
import { api, ApiError } from "@/lib/api";
import { DEPARTMENTS } from "@/lib/departments";
import type { ChatMessageOut, DepartmentKey } from "@/lib/types";
import { useSession } from "@/context/SessionContext";
import { MessageBubble, TypingIndicator } from "@/components/MessageBubble";

function ChatPageInner() {
  const { user } = useSession();
  const params = useParams<{ key: string }>();
  const router = useRouter();
  const searchParams = useSearchParams();
  const deptKey = params.key as DepartmentKey;
  const dept = DEPARTMENTS[deptKey];

  const [messages, setMessages] = useState<ChatMessageOut[]>([]);
  const [online, setOnline] = useState<boolean | null>(null);
  const [draft, setDraft] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bodyRef = useRef<HTMLDivElement>(null);
  const prefillHandled = useRef(false);

  useEffect(() => {
    if (!user || !dept) return;
    api.getChatHistory(user.company_id, deptKey).then(setMessages).catch(() => undefined);
    api
      .getAgentsStatus()
      .then((statuses) => {
        const match = statuses.find((s) => s.department === deptKey);
        setOnline(match?.online ?? false);
      })
      .catch(() => setOnline(false));
  }, [user, deptKey, dept]);

  useEffect(() => {
    bodyRef.current?.scrollTo({ top: bodyRef.current.scrollHeight, behavior: "smooth" });
  }, [messages, sending]);

  useEffect(() => {
    const prompt = searchParams.get("prompt");
    if (prompt && !prefillHandled.current) {
      prefillHandled.current = true;
      void send(prompt);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  async function send(text: string) {
    if (!user || !text.trim() || sending) return;
    setError(null);
    setDraft("");
    setSending(true);
    const optimisticUser: ChatMessageOut = {
      id: `local-${Date.now()}`,
      department: deptKey,
      sender: "user",
      content: text,
      created_at: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, optimisticUser]);

    try {
      const res = await api.sendChatMessage({
        companyId: user.company_id,
        userId: user.id,
        department: deptKey,
        message: text,
      });
      setMessages((prev) => [...prev, res.reply]);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to reach the agent.");
    } finally {
      setSending(false);
    }
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    void send(draft);
  }

  if (!user || !dept) return null;

  return (
    <div className="chat" data-dept={deptKey}>
      <div className="chat-head">
        <div className="chat-agent">
          <div className="exec-avatar lg">
            <div className="ring" />
            <span>{dept.name[0]}</span>
          </div>
          <div>
            <h2>
              Agent{" "}
              {online === null ? null : online ? (
                <span className="online-pill">● online</span>
              ) : (
                <span className="online-pill offline">● offline</span>
              )}
            </h2>
            <p className="muted">{dept.name}</p>
          </div>
        </div>
        <button
          className="btn ghost"
          onClick={() => router.push(deptKey === "executive" ? "/team" : `/dept/${deptKey}`)}
        >
          ← Back
        </button>
      </div>

      <div className="chat-body" ref={bodyRef}>
        {messages.length === 0 && (
          <div className="chat-welcome">
            <div className="exec-avatar xl">
              <div className="ring" />
              <span>{dept.name[0]}</span>
            </div>
            <h3>Hi, I&rsquo;m your {dept.name} agent.</h3>
            <p className="muted">Ask me anything about {dept.name.toLowerCase()}.</p>
            <div className="prompt-grid">
              {dept.suggestions.map((s) => (
                <button key={s} className="prompt-chip" onClick={() => void send(s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>
        )}

        <div className="chat-messages">
          {messages.map((m) => (
            <MessageBubble
              key={m.id}
              message={m}
              dept={dept}
              userInitials={user.initials}
              userCls={DEPARTMENTS[user.department].cls}
            />
          ))}
          {sending && <TypingIndicator dept={dept} />}
        </div>
      </div>

      {error && <div className="error-banner">{error}</div>}

      <form className="chat-input-wrap" onSubmit={handleSubmit}>
        <div className="chat-input">
          <textarea
            rows={1}
            placeholder={`Message your ${dept.name} agent…`}
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                void send(draft);
              }
            }}
          />
          <button type="submit" className="send-btn" disabled={sending || !draft.trim()} title="Send">
            <svg viewBox="0 0 24 24">
              <path d="M3 11 21 3l-8 18-2-7-8-3Z" />
            </svg>
          </button>
        </div>
        <span className="chat-hint">
          Backed by a live agent · tool logic is still being implemented · Enter to send, Shift+Enter
          for newline
        </span>
      </form>
    </div>
  );
}

export default function ChatPage() {
  return (
    <Suspense fallback={<div className="centered-loading">Loading chat…</div>}>
      <ChatPageInner />
    </Suspense>
  );
}
