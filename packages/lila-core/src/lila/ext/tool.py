from collections.abc import Callable
from dataclasses import dataclass

TOOL_MARK = "__lila_tool__"


class ToolError(RuntimeError):
    """A tool failed. The one error an adapter raises for a failed call."""


@dataclass(frozen=True)
class ToolSpec:
    pass


def tool[T: Callable[..., object]](fn: T) -> T:
    """Mark a function as a tool."""
    spec = ToolSpec()
    setattr(fn, TOOL_MARK, spec)
    return fn
