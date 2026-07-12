"""Seed a demo company + the seven demo users used by the frontend login screen.

Mirrors frontend_temp/app.js's USERS/DEPTS constants so the frontend's login
cards line up with real rows once the frontend switches from static data to
`GET /api/v1/users`. Run with: `python -m scripts.seed_demo_workspace`.
"""

import asyncio

from app.db import init_db, session_scope
from app.models import Company, User

DEMO_USERS = [
    ("Minh Hoàng", "MH", "Chief Executive Officer", "manager", "executive"),
    ("Lan Phạm", "LP", "Finance Analyst", "employee", "finance"),
    ("Trang Nguyễn", "TN", "Marketing Lead", "employee", "marketing"),
    ("Huy Trần", "HT", "Operations Coordinator", "employee", "operations"),
    ("Mai Lê", "ML", "HR Specialist", "employee", "hr"),
    ("Đức Vũ", "ĐV", "Compliance Officer", "employee", "compliance"),
    ("Khoa Đỗ", "KĐ", "Data Analyst", "employee", "bi"),
]


async def seed() -> None:
    await init_db()
    async with session_scope() as session:
        company = Company(
            legal_name="Đại Việt Trading JSC",
            industry="Wholesale & Distribution",
            tax_id="0312-XXX-456",
            employee_count=48,
            annual_revenue_vnd=58_000_000_000,
            digital_maturity_level=3,
        )
        session.add(company)
        await session.flush()

        for full_name, initials, title, role, department in DEMO_USERS:
            session.add(
                User(
                    company_id=company.id,
                    full_name=full_name,
                    initials=initials,
                    title=title,
                    role=role,
                    department=department,
                )
            )
        await session.commit()
        print(f"Seeded company {company.id} with {len(DEMO_USERS)} users.")


if __name__ == "__main__":
    asyncio.run(seed())
