from pydantic import BaseModel, JsonValue

from lila.core.engine.types import ExecutionId, TaskId
from lila.core.graph.types import NodeId


class Task(BaseModel):
    id: TaskId
    execution_id: ExecutionId
    node_id: NodeId
    attempt: int


class TaskResult(BaseModel):
    ok: bool
    output: JsonValue
    error: str | None = None
