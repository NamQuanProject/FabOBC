-- FabOPC sample data for UI testing — no backend agents required.
--
-- Populates one demo company ("Đại Việt Trading JSC") with the same 7 users,
-- KPIs, and tasks shown in frontend_temp's static mockup, so the real
-- frontend has something to render immediately: login screen, department
-- dashboards, team overview, and business profile.
--
-- Run this AFTER sql/init_postgresql.sql has created the tables (either via
-- `psql ... -f sql/init_postgresql.sql`, the Supabase SQL Editor, or by
-- just starting the FastAPI app once — app.db.init_db() creates them too).
--
-- Run in the Supabase SQL Editor, or:
--   psql "postgresql://postgres:<password>@db.<project-ref>.supabase.co:5432/postgres" -f sql/seed_sample_data.sql
--
-- Idempotent: re-running deletes the demo company (cascades to every child
-- row via FK ON DELETE CASCADE) and re-inserts fresh, so this is safe to use
-- as a "reset my demo data" script while iterating on the UI.

begin;

delete from companies where id = '00000000-0000-4000-8000-000000000001';

insert into companies (id, legal_name, industry, tax_id, employee_count, annual_revenue_vnd, digital_maturity_level)
values (
    '00000000-0000-4000-8000-000000000001',
    'Đại Việt Trading JSC',
    'Wholesale & Distribution',
    '0312-XXX-456',
    48,
    58000000000,
    3
);

-- ---------------------------------------------------------------------
-- Users — mirrors frontend_temp/app.js's USERS list.
-- ---------------------------------------------------------------------
insert into users (id, company_id, full_name, initials, title, role, department, email) values
    ('00000000-0000-4000-8000-000000000101', '00000000-0000-4000-8000-000000000001', 'Minh Hoàng',   'MH', 'Chief Executive Officer', 'manager',  'executive',  'ceo@daiviettrading.vn'),
    ('00000000-0000-4000-8000-000000000102', '00000000-0000-4000-8000-000000000001', 'Lan Phạm',     'LP', 'Finance Analyst',         'employee', 'finance',    'finance@daiviettrading.vn'),
    ('00000000-0000-4000-8000-000000000103', '00000000-0000-4000-8000-000000000001', 'Trang Nguyễn', 'TN', 'Marketing Lead',          'employee', 'marketing',  'marketing@daiviettrading.vn'),
    ('00000000-0000-4000-8000-000000000104', '00000000-0000-4000-8000-000000000001', 'Huy Trần',     'HT', 'Operations Coordinator',  'employee', 'operations', 'operations@daiviettrading.vn'),
    ('00000000-0000-4000-8000-000000000105', '00000000-0000-4000-8000-000000000001', 'Mai Lê',       'ML', 'HR Specialist',           'employee', 'hr',         'hr@daiviettrading.vn'),
    ('00000000-0000-4000-8000-000000000106', '00000000-0000-4000-8000-000000000001', 'Đức Vũ',       'ĐV', 'Compliance Officer',      'employee', 'compliance', 'compliance@daiviettrading.vn'),
    ('00000000-0000-4000-8000-000000000107', '00000000-0000-4000-8000-000000000001', 'Khoa Đỗ',      'KĐ', 'Data Analyst',            'employee', 'bi',         'bi@daiviettrading.vn');

-- ---------------------------------------------------------------------
-- KPIs — mirrors frontend_temp/app.js's DEPTS[*].kpis.
-- ---------------------------------------------------------------------
insert into department_kpis (company_id, department, label, value, trend_label, trend_direction) values
    ('00000000-0000-4000-8000-000000000001', 'finance', 'Monthly Revenue', '₫4.82B',   '▲ 12.4%',  'up'),
    ('00000000-0000-4000-8000-000000000001', 'finance', 'Net Margin',      '18.6%',    '▼ 2.1%',   'down'),
    ('00000000-0000-4000-8000-000000000001', 'finance', 'Cash Runway',     '14.2 mo',  '● stable', 'flat'),
    ('00000000-0000-4000-8000-000000000001', 'finance', 'Overdue AR',      '₫186M',    '▼ ₫40M',   'up'),

    ('00000000-0000-4000-8000-000000000001', 'marketing', 'Reach (30d)',  '248K',  '▲ 22%',  'up'),
    ('00000000-0000-4000-8000-000000000001', 'marketing', 'Engagement',   '6.4%',  '▲ 1.1%', 'up'),
    ('00000000-0000-4000-8000-000000000001', 'marketing', 'Leads',        '312',   '▲ 18',   'up'),
    ('00000000-0000-4000-8000-000000000001', 'marketing', 'CAC',          '₫84K',  '▼ 6%',   'up'),

    ('00000000-0000-4000-8000-000000000001', 'operations', 'On-time Delivery', '94%',      '▼ 3%',      'down'),
    ('00000000-0000-4000-8000-000000000001', 'operations', 'Open Orders',      '128',      '▲ 12',      'flat'),
    ('00000000-0000-4000-8000-000000000001', 'operations', 'Inventory Turn',   '6.1×',     '▲ 0.4',     'up'),
    ('00000000-0000-4000-8000-000000000001', 'operations', 'Supplier SLA',     '2 issues', '⚠ delay',   'down'),

    ('00000000-0000-4000-8000-000000000001', 'hr', 'Headcount',       '48',  '▲ 2',      'up'),
    ('00000000-0000-4000-8000-000000000001', 'hr', 'Open Roles',      '3',   '● hiring', 'flat'),
    ('00000000-0000-4000-8000-000000000001', 'hr', 'Attrition (12m)', '8%',  '▼ 2%',     'up'),
    ('00000000-0000-4000-8000-000000000001', 'hr', 'eNPS',            '+41', '▲ 5',      'up'),

    ('00000000-0000-4000-8000-000000000001', 'compliance', 'Compliance Score', '96/100', '▲ 2',        'up'),
    ('00000000-0000-4000-8000-000000000001', 'compliance', 'Next Deadline',    '9 days', 'VAT 20 Jun', 'down'),
    ('00000000-0000-4000-8000-000000000001', 'compliance', 'VAT Payable',      '₫312M',  'Q2 est.',    'flat'),
    ('00000000-0000-4000-8000-000000000001', 'compliance', 'Filings YTD',      '17',     '100% on time', 'up'),

    ('00000000-0000-4000-8000-000000000001', 'bi', 'Data Sources',   '5 synced', '● live', 'flat'),
    ('00000000-0000-4000-8000-000000000001', 'bi', 'Insights (7d)',  '23',       '▲ 8',    'up'),
    ('00000000-0000-4000-8000-000000000001', 'bi', 'Churn Risk',     '4 accts',  '⚠ 61%',  'down'),
    ('00000000-0000-4000-8000-000000000001', 'bi', 'Forecast Acc.',  '92%',      '▲ 3%',   'up');

-- ---------------------------------------------------------------------
-- Tasks — mirrors frontend_temp/app.js's DEPTS[*].tasks.
-- ---------------------------------------------------------------------
insert into department_tasks (company_id, department, title, status, due_label) values
    ('00000000-0000-4000-8000-000000000001', 'finance', 'Reconcile May bank statements',            'In progress', 'Today'),
    ('00000000-0000-4000-8000-000000000001', 'finance', 'Model Q3 margin scenarios for CEO',         'In progress', 'Tomorrow'),
    ('00000000-0000-4000-8000-000000000001', 'finance', 'Approve 3 vendor payments',                 'Waiting',     '16 Jun'),
    ('00000000-0000-4000-8000-000000000001', 'finance', 'Close monthly books',                       'Scheduled',   '30 Jun'),

    ('00000000-0000-4000-8000-000000000001', 'marketing', 'Draft summer promo for Facebook + Zalo',  'In progress', 'Today'),
    ('00000000-0000-4000-8000-000000000001', 'marketing', 'Schedule weekly content calendar',        'In progress', 'Today'),
    ('00000000-0000-4000-8000-000000000001', 'marketing', 'Review LinkedIn case study',               'Waiting',     '18 Jun'),
    ('00000000-0000-4000-8000-000000000001', 'marketing', 'A/B test email subject lines',             'Scheduled',   '20 Jun'),

    ('00000000-0000-4000-8000-000000000001', 'operations', 'Resolve supplier delay (3 orders)',       'Escalated',   'Today'),
    ('00000000-0000-4000-8000-000000000001', 'operations', 'Rebalance SKU-204 inventory buffer',      'In progress', 'Today'),
    ('00000000-0000-4000-8000-000000000001', 'operations', 'Negotiate carrier rate increase',         'Waiting',     '19 Jun'),
    ('00000000-0000-4000-8000-000000000001', 'operations', 'Audit warehouse cycle counts',            'Scheduled',   '25 Jun'),

    ('00000000-0000-4000-8000-000000000001', 'hr', 'Screen candidates for Sales role',                'In progress', 'Today'),
    ('00000000-0000-4000-8000-000000000001', 'hr', 'Schedule 3 interviews',                            'In progress', 'Tomorrow'),
    ('00000000-0000-4000-8000-000000000001', 'hr', 'Process June payroll',                             'Scheduled',   '28 Jun'),
    ('00000000-0000-4000-8000-000000000001', 'hr', 'Renew health-insurance plan',                      'Waiting',     '30 Jun'),

    ('00000000-0000-4000-8000-000000000001', 'compliance', 'Prepare VAT declaration (01/GTGT)',       'Action needed', '20 Jun'),
    ('00000000-0000-4000-8000-000000000001', 'compliance', 'Finalize PIT withholding',                 'Draft ready',   '20 Jun'),
    ('00000000-0000-4000-8000-000000000001', 'compliance', 'Director sign-off on filings',             'Waiting',       '18 Jun'),
    ('00000000-0000-4000-8000-000000000001', 'compliance', 'File Corporate Income Tax',                'Scheduled',     '30 Jul'),

    ('00000000-0000-4000-8000-000000000001', 'bi', 'Refresh unified data warehouse',                  'In progress', 'Today'),
    ('00000000-0000-4000-8000-000000000001', 'bi', 'Investigate churn signal (4 accounts)',           'In progress', 'Today'),
    ('00000000-0000-4000-8000-000000000001', 'bi', 'Build Q3 revenue forecast',                       'Waiting',     '21 Jun'),
    ('00000000-0000-4000-8000-000000000001', 'bi', 'Connect contract repository',                     'Syncing',     '17 Jun');

-- ---------------------------------------------------------------------
-- Knowledge sources — mirrors the Business Profile screen mockup.
-- ---------------------------------------------------------------------
insert into knowledge_sources (company_id, title, source_type, indexed) values
    ('00000000-0000-4000-8000-000000000001', 'Company Handbook.pdf', 'doc', true),
    ('00000000-0000-4000-8000-000000000001', 'Price List 2026.xlsx', 'spreadsheet', true),
    ('00000000-0000-4000-8000-000000000001', 'Financial Statements Q1–Q2', 'accounting', true);

-- ---------------------------------------------------------------------
-- Compliance obligations — a few upcoming filings for the OPC Profile Object.
-- ---------------------------------------------------------------------
insert into compliance_obligations (company_id, obligation_code, description, due_date, responsible_department, risk_level, status) values
    ('00000000-0000-4000-8000-000000000001', '01/GTGT', 'VAT declaration for the current period',        now() + interval '9 days',  'compliance', 'high',   'action_needed'),
    ('00000000-0000-4000-8000-000000000001', 'PIT',     'Personal income tax withholding',                now() + interval '9 days',  'compliance', 'medium', 'draft_ready'),
    ('00000000-0000-4000-8000-000000000001', 'CIT',     'Quarterly corporate income tax filing',          now() + interval '48 days', 'compliance', 'low',    'scheduled');

-- ---------------------------------------------------------------------
-- OPC Profile Object — minimal seed so /api/v1/companies/{id}/opc-profile
-- returns something realistic instead of an empty shell.
-- ---------------------------------------------------------------------
insert into opc_profiles (company_id, profile) values (
    '00000000-0000-4000-8000-000000000001',
    '{
        "identity": {
            "company_id": "00000000-0000-4000-8000-000000000001",
            "legal_name": "Đại Việt Trading JSC",
            "industry": "Wholesale & Distribution",
            "headquarters": "Hồ Chí Minh City",
            "tax_id": "0312-XXX-456",
            "employee_count": 48,
            "annual_revenue_vnd": 58000000000,
            "digital_maturity_level": 3
        },
        "departments": {
            "operations": {
                "department": "operations",
                "agent_persona": "Forge",
                "active_signals": ["supplier_delay:3_orders"],
                "notes": {}
            },
            "compliance": {
                "department": "compliance",
                "agent_persona": "Lex",
                "active_signals": ["vat_filing_due_9d"],
                "notes": {}
            }
        },
        "obligations": [],
        "knowledge_sources": []
    }'::jsonb
);

commit;
