import type { ChatMessageOut } from "@/lib/types";
import type { DepartmentMeta } from "@/lib/departments";

export function MessageBubble({
  message,
  dept,
  userInitials,
  userCls,
}: {
  message: ChatMessageOut;
  dept: DepartmentMeta;
  userInitials: string;
  userCls: string;
}) {
  if (message.sender === "user") {
    return (
      <div className="msg user">
        <div className="bubble">{message.content}</div>
        <div className={`avatar sm ${userCls}`}>{userInitials}</div>
      </div>
    );
  }
  return (
    <div className="msg bot reveal">
      <div className={`msg-ava ${dept.cls}`}>{dept.name[0]}</div>
      <div className="bubble bot">{message.content}</div>
    </div>
  );
}

export function TypingIndicator({ dept }: { dept: DepartmentMeta }) {
  return (
    <div className="msg bot">
      <div className={`msg-ava ${dept.cls}`}>{dept.name[0]}</div>
      <div className="bubble bot typing-bubble">
        <span />
        <span />
        <span />
      </div>
    </div>
  );
}
