"""CRUD for the persisted OPC Profile Object (opc_profiles.profile JSONB),
via the Supabase client rather than a direct Postgres connection.

Deserializes into core.opc_profile.OPCProfileObject for validation. Agents
mutate this indirectly through the orchestration MCP server's
`update_opc_profile` tool (not yet implemented); this service is what that
tool would eventually call into.
"""

from supabase import AsyncClient

from app.tables import OPC_PROFILES
from core.opc_profile import CompanyIdentity, OPCProfileObject


async def get_or_create_profile(client: AsyncClient, company_id: str) -> OPCProfileObject:
    result = (
        await client.table(OPC_PROFILES)
        .select("profile")
        .eq("company_id", company_id)
        .maybe_single()
        .execute()
    )
    if result is None or result.data is None:
        profile = OPCProfileObject(identity=CompanyIdentity(company_id=company_id, legal_name=""))
        await client.table(OPC_PROFILES).insert(
            {"company_id": company_id, "profile": profile.model_dump(mode="json")}
        ).execute()
        return profile
    return OPCProfileObject.model_validate(result.data["profile"])


async def save_profile(
    client: AsyncClient, company_id: str, profile: OPCProfileObject
) -> OPCProfileObject:
    await client.table(OPC_PROFILES).upsert(
        {"company_id": company_id, "profile": profile.model_dump(mode="json")},
        on_conflict="company_id",
    ).execute()
    return profile
