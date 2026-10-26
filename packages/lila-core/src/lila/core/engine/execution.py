from pydantic import BaseModel

from lila.core.engine.types import ExecutionId, ExecutionPriority
from lila.core.graph.base import Graph


class Execution(BaseModel):
    id: ExecutionId
    graph: Graph
    priority: ExecutionPriority
