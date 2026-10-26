from pydantic import BaseModel, JsonValue

from lila.core.engine.types import ExecutionId
from lila.core.graph.base import Graph


class Execution(BaseModel):
    id: ExecutionId
    inputs: JsonValue
    graph: Graph
