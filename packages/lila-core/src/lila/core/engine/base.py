from pydantic import JsonValue

from lila.core.engine.types import ExecutionId, ExecutionPriority
from lila.core.graph.base import Graph


class Engine:
    def __init__(self):
        pass

    # region: running a graph
    def submit(
        self, graph: Graph, input: JsonValue, priority: ExecutionPriority
    ) -> ExecutionId: ...

    # endregion: running a graph

    def on_event(self, event: None) -> None: ...
    def on_complete(self, task: None, result: None) -> None: ...
    def on_cancel(self, execution_id: ExecutionId) -> None: ...
