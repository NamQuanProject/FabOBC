"""Supabase table name constants — mirrors sql/init_postgresql.sql.

Kept as plain strings (no ORM) since all access goes through the Supabase
client's `.table(name)` query builder rather than SQLAlchemy models.
"""

COMPANIES = "companies"
USERS = "users"
OPC_PROFILES = "opc_profiles"
DEPARTMENT_KPIS = "department_kpis"
DEPARTMENT_TASKS = "department_tasks"
CHAT_MESSAGES = "chat_messages"
KNOWLEDGE_SOURCES = "knowledge_sources"
COMPLIANCE_OBLIGATIONS = "compliance_obligations"
