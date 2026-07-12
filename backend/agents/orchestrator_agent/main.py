"""Serve Orion (Orchestrator Agent) as an A2A server on its configured port.

The FastAPI gateway's /api/v1/agents/orchestrate endpoint (see
app/services/a2a_client.py) talks to this server. Start the six department
agents first (agents/{finance,marketing,operations,hr,compliance,bi}_agent
.main), then this one:

    python -m agents.finance_agent.main &
    python -m agents.marketing_agent.main &
    python -m agents.operations_agent.main &
    python -m agents.hr_agent.main &
    python -m agents.compliance_agent.main &
    python -m agents.bi_agent.main &
    python -m agents.orchestrator_agent.main
"""

import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from agents.orchestrator_agent.agent import root_agent
from core.config import get_settings

settings = get_settings()

a2a_app = to_a2a(root_agent, port=settings.orchestrator_agent_port)


def main() -> None:
    print(
        f"Starting Orion (Orchestrator Agent) A2A server on "
        f"{settings.agent_host}:{settings.orchestrator_agent_port} ..."
    )
    uvicorn.run(a2a_app, host=settings.agent_host, port=settings.orchestrator_agent_port)


if __name__ == "__main__":
    main()
