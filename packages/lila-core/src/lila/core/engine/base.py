from pydantic import JsonValue

from lila.core.engine.store.sqlite import SqliteStore
from lila.core.engine.types import ExecutionId
from lila.core.graph.base import Graph


class Engine:
    def __init__(self, store: SqliteStore):
        self._store = store

    async def submit(self, inputs: JsonValue, graph: Graph) -> ExecutionId:
        return await self._store.create_execution(inputs=inputs, graph=graph)
