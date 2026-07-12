// Mirrors backend/app/schema/*.py response shapes.

export type DepartmentKey =
  | "executive"
  | "finance"
  | "marketing"
  | "operations"
  | "hr"
  | "compliance"
  | "bi";

export interface UserOut {
  id: string;
  company_id: string;
  full_name: string;
  initials: string;
  title: string;
  role: "manager" | "employee";
  department: DepartmentKey;
  email: string | null;
}

export interface KpiOut {
  id: string;
  department: string;
  label: string;
  value: string;
  trend_label: string | null;
  trend_direction: "up" | "down" | "flat" | null;
}

export interface TaskOut {
  id: string;
  department: string;
  title: string;
  status: string;
  due_label: string | null;
  created_at: string;
}

export interface DepartmentDashboard {
  department: string;
  agent_persona: string;
  agent_role_title: string;
  insight: string;
  kpis: KpiOut[];
  tasks: TaskOut[];
}

export interface KnowledgeSourceOut {
  id: string;
  title: string;
  source_type: string;
  indexed: boolean;
}

export interface BusinessProfileOut {
  company_id: string;
  legal_name: string;
  industry: string | null;
  tax_id: string | null;
  employee_count: number | null;
  annual_revenue_vnd: number | null;
  digital_maturity_level: number | null;
  knowledge_sources: KnowledgeSourceOut[];
}

export interface AgentStatusOut {
  department: string;
  persona_name: string;
  role_title: string;
  online: boolean;
  url: string;
}

export interface ChatMessageOut {
  id: string;
  department: string;
  sender: "user" | "agent";
  content: string;
  created_at: string;
}

export interface ChatResponse {
  department: string;
  reply: ChatMessageOut;
}
