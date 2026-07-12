-- FabOPC schema bootstrap for Supabase/Postgres.
-- Mirrors backend/app/models.py. Run manually with:
--   psql "postgresql://USER:PASSWORD@HOST:PORT/DB?sslmode=require" -f sql/init_postgresql.sql
-- (app.db.init_db() also creates these automatically via SQLAlchemy on startup.)

create extension if not exists "uuid-ossp";

create table if not exists companies (
    id uuid primary key default uuid_generate_v4(),
    legal_name text not null,
    industry text,
    tax_id text,
    employee_count integer,
    annual_revenue_vnd numeric,
    digital_maturity_level integer check (digital_maturity_level between 1 and 5),
    created_at timestamptz not null default now()
);

create table if not exists users (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid not null references companies(id) on delete cascade,
    full_name text not null,
    initials varchar(4) not null,
    title text not null,
    role text not null check (role in ('manager', 'employee')),
    department text not null,
    email text unique
);

create table if not exists opc_profiles (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid not null unique references companies(id) on delete cascade,
    profile jsonb not null default '{}'::jsonb,
    updated_at timestamptz not null default now()
);

create table if not exists department_kpis (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid not null references companies(id) on delete cascade,
    department text not null,
    label text not null,
    value text not null,
    trend_label text,
    trend_direction text check (trend_direction in ('up', 'down', 'flat'))
);

create table if not exists department_tasks (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid not null references companies(id) on delete cascade,
    department text not null,
    title text not null,
    status text not null,
    due_label text,
    created_at timestamptz not null default now()
);

create table if not exists chat_messages (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid not null references companies(id) on delete cascade,
    user_id uuid not null references users(id) on delete cascade,
    department text not null,
    sender text not null check (sender in ('user', 'agent')),
    content text not null,
    created_at timestamptz not null default now()
);

create table if not exists knowledge_sources (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid not null references companies(id) on delete cascade,
    title text not null,
    source_type text not null,
    indexed boolean not null default false,
    created_at timestamptz not null default now()
);

create table if not exists compliance_obligations (
    id uuid primary key default uuid_generate_v4(),
    company_id uuid not null references companies(id) on delete cascade,
    obligation_code text not null,
    description text not null,
    due_date timestamptz,
    responsible_department text,
    risk_level text,
    status text not null default 'pending'
);

create index if not exists idx_users_company on users(company_id);
create index if not exists idx_kpis_company_dept on department_kpis(company_id, department);
create index if not exists idx_tasks_company_dept on department_tasks(company_id, department);
create index if not exists idx_chat_company_dept on chat_messages(company_id, department);
create index if not exists idx_obligations_company on compliance_obligations(company_id);
