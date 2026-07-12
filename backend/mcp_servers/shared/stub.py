"""Shared helper for tool bodies that are structured but not yet implemented.

Every MCP tool in this codebase is signature-complete (typed args, typed
return model, real docstring describing the business logic from the FabOPC
proposal) but raises NotImplementedTool instead of executing real logic.
Wiring a tool up later means replacing the `raise not_implemented(...)` line
with the actual implementation — the signature and callers do not change.
"""


class NotImplementedTool(NotImplementedError):
    def __init__(self, tool_name: str, spec: str):
        super().__init__(
            f"Tool '{tool_name}' is structured but not yet implemented. "
            f"Intended behavior: {spec}"
        )


def not_implemented(tool_name: str, spec: str) -> NotImplementedTool:
    return NotImplementedTool(tool_name, spec)
