import type { DepartmentKey } from "./types";

// Static per-department presentation metadata (colors, icon paths, chat
// suggestion prompts). Backend-sourced data (KPIs, tasks, live insight,
// agent online status) comes from the API — see lib/api.ts.
export interface DepartmentMeta {
  key: DepartmentKey;
  name: string;
  short: string;
  cls: string;
  icon: string;
  suggestions: string[];
}

export const DEPARTMENTS: Record<DepartmentKey, DepartmentMeta> = {
  executive: {
    key: "executive",
    name: "Executive Office",
    short: "Executive",
    cls: "comp",
    icon: "M3 3h18v4H3V3Zm0 7h11v11H3V10Zm14 0h4v11h-4V10Z",
    suggestions: [
      "Give me the morning briefing",
      "What needs my approval today?",
      "Why did margin drop?",
      "Summarize risks across all departments",
    ],
  },
  finance: {
    key: "finance",
    name: "Finance",
    short: "Finance",
    cls: "finance",
    icon: "M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm.9 15.4v1.3h-1.6v-1.3c-1.4-.2-2.6-1-2.7-2.6h1.7c.1.7.6 1.2 1.8 1.2 1 0 1.6-.4 1.6-1.1 0-.6-.4-.9-1.8-1.2-1.8-.4-3-1-3-2.6 0-1.3 1-2.1 2.4-2.4V7h1.6v1.3c1.4.3 2.2 1.2 2.3 2.4h-1.7c-.1-.7-.5-1.1-1.5-1.1s-1.4.4-1.4 1c0 .5.4.8 1.8 1.1 1.9.4 3 1 3 2.7 0 1.3-1 2.2-2.6 2.5Z",
    suggestions: [
      "What's our cash position?",
      "Model Q3 margin scenarios",
      "List overdue receivables",
      "Draft a budget summary for the CEO",
    ],
  },
  marketing: {
    key: "marketing",
    name: "Marketing",
    short: "Marketing",
    cls: "mkt",
    icon: "M3 11v2h2.6l9.4 4V7L5.6 11H3Zm14 .5a3 3 0 0 0-1.5-2.6v5.2A3 3 0 0 0 17 11.5ZM18 5l-1.4 1.4a7 7 0 0 1 0 8.2L18 16a9 9 0 0 0 0-11Z",
    suggestions: [
      "Write a summer promo for Facebook",
      "How are our campaigns performing?",
      "Suggest content for next week",
      "Which audience converts best?",
    ],
  },
  operations: {
    key: "operations",
    name: "Operations",
    short: "Operations",
    cls: "ops",
    icon: "M19.4 13a7.8 7.8 0 0 0 0-2l2-1.6-2-3.4-2.4 1a7.6 7.6 0 0 0-1.7-1l-.4-2.6H10l-.4 2.6a7.6 7.6 0 0 0-1.7 1l-2.4-1-2 3.4L3.6 11a7.8 7.8 0 0 0 0 2l-2 1.6 2 3.4 2.4-1a7.6 7.6 0 0 0 1.7 1l.4 2.6h4l.4-2.6a7.6 7.6 0 0 0 1.7-1l2.4 1 2-3.4-2-1.6ZM12 15.5a3.5 3.5 0 1 1 0-7 3.5 3.5 0 0 1 0 7Z",
    suggestions: [
      "What's the status of the supplier delay?",
      "Show me inventory health",
      "Which orders are at risk?",
      "Optimize our delivery routes",
    ],
  },
  hr: {
    key: "hr",
    name: "Human Resources",
    short: "HR",
    cls: "hr",
    icon: "M16 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm-8 0a3 3 0 1 0 0-6 3 3 0 0 0 0 6Zm0 2c-2.7 0-6 1.3-6 4v2h8v-2c0-1 .4-1.9 1-2.6A9 9 0 0 0 8 13Zm8 0c-.6 0-1.2 0-1.7.1 1 .8 1.7 1.8 1.7 2.9v2h6v-2c0-2.7-3.3-4-6-4Z",
    suggestions: [
      "How is hiring going?",
      "Draft a job post for the Sales role",
      "Show me team headcount",
      "Any retention risks?",
    ],
  },
  compliance: {
    key: "compliance",
    name: "Compliance",
    short: "Compliance",
    cls: "comp",
    icon: "M12 2 4 5v6c0 5 3.4 9.7 8 11 4.6-1.3 8-6 8-11V5l-8-3Zm-1 14-4-4 1.4-1.4L11 13.2l4.6-4.6L17 10l-6 6Z",
    suggestions: [
      "What tax filings are due?",
      "Calculate our VAT payable",
      "Are we missing any deductions?",
      "Check our compliance status",
    ],
  },
  bi: {
    key: "bi",
    name: "Business Intelligence",
    short: "BI",
    cls: "bi",
    icon: "M3 3v18h18v-2H5V3H3Zm4 12h2v3H7v-3Zm4-6h2v9h-2V9Zm4 3h2v6h-2v-6Zm4-7h2v13h-2V5Z",
    suggestions: [
      "What are the top insights this week?",
      "Which customers are at risk of churning?",
      "Forecast next quarter revenue",
      "Where are we losing money?",
    ],
  },
};

export const DEPARTMENT_ORDER: DepartmentKey[] = [
  "finance",
  "marketing",
  "operations",
  "hr",
  "compliance",
  "bi",
];
