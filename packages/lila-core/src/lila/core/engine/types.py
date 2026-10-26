from enum import IntEnum
from typing import Literal

type ExecutionId = str
type ExecutionStatus = Literal["running", "blocked", "done", "failed", "cancelled"]

type TaskId = str


class ExecutionPriority(IntEnum):
    BACKGROUND = 0
    INTERACTIVE = 10
