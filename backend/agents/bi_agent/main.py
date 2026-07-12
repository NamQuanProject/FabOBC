"""Serve Echo (BI Agent) as an A2A server on its configured port.

Run standalone: `python -m agents.bi_agent.main`
"""

import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from agents.bi_agent.agent import root_agent
from core.config import get_settings

settings = get_settings()

a2a_app = to_a2a(root_agent, port=settings.bi_agent_port)


def main() -> None:
    print(
        f"Starting Echo (BI Agent) A2A server on "
        f"{settings.agent_host}:{settings.bi_agent_port} ..."
    )
    uvicorn.run(a2a_app, host=settings.agent_host, port=settings.bi_agent_port)


if __name__ == "__main__":
    main()
