from lila.core.graph.types import NodeId


class ParseError(ValueError):
    """A malformed graph file. Carries the offending location"""

    def __init__(
        self, message: str, *, line: int | None = None, node_id: NodeId | None = None
    ) -> None:
        self._metadata = {"line": line, "node_id": node_id}
        super().__init__(f"{message} {str(self._metadata)}")
