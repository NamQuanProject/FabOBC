export function ExecutiveCard({
  personaInitial,
  tag,
  message,
  children,
}: {
  personaInitial: string;
  tag: string;
  message: string;
  children?: React.ReactNode;
}) {
  return (
    <div className="exec-card">
      <div className="exec-avatar">
        <div className="ring" />
        <span>{personaInitial}</span>
      </div>
      <div className="exec-body">
        <div className="exec-tag">{tag}</div>
        <p>{message}</p>
        {children && <div className="exec-chips">{children}</div>}
      </div>
    </div>
  );
}
