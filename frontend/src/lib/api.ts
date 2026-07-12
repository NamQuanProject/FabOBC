import type {
  AgentStatusOut,
  BusinessProfileOut,
  ChatMessageOut,
  ChatResponse,
  DepartmentDashboard,
  UserOut,
} from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!res.ok) {
    const body = await res.text().catch(() => "");
    throw new ApiError(res.status, body || `Request to ${path} failed with ${res.status}`);
  }
  return res.json() as Promise<T>;
}

export const api = {
  listUsers: () => request<UserOut[]>("/api/v1/users"),

  login: (userId: string) =>
    request<{ user: UserOut }>("/api/v1/auth/login", {
      method: "POST",
      body: JSON.stringify({ user_id: userId }),
    }),

  getDepartmentDashboard: (companyId: string, department: string) =>
    request<DepartmentDashboard>(
      `/api/v1/companies/${companyId}/departments/${department}`
    ),

  getBusinessProfile: (companyId: string) =>
    request<BusinessProfileOut>(`/api/v1/companies/${companyId}/business-profile`),

  getAgentsStatus: () => request<AgentStatusOut[]>("/api/v1/agents/status"),

  getChatHistory: (companyId: string, department: string) =>
    request<ChatMessageOut[]>(
      `/api/v1/companies/${companyId}/departments/${department}/messages`
    ),

  sendChatMessage: (params: {
    companyId: string;
    userId: string;
    department: string;
    message: string;
  }) =>
    request<ChatResponse>("/api/v1/agents/orchestrate", {
      method: "POST",
      body: JSON.stringify({
        company_id: params.companyId,
        user_id: params.userId,
        department: params.department,
        message: params.message,
      }),
    }),
};

export { ApiError };
