"""Serve Nova (Marketing Agent) as an A2A server on its configured port.

Run standalone: `python -m agents.marketing_agent.main`
"""

import uvicorn
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from agents.marketing_agent.agent import root_agent
from core.config import get_settings

settings = get_settings()

a2a_app = to_a2a(root_agent, port=settings.marketing_agent_port)


def main() -> None:
    print(
        f"Starting Nova (Marketing Agent) A2A server on "
        f"{settings.agent_host}:{settings.marketing_agent_port} ..."
    )
    uvicorn.run(a2a_app, host=settings.agent_host, port=settings.marketing_agent_port)


if __name__ == "__main__":
    main()
