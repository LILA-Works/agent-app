from enum import IntEnum

type ExecutionId = str

type TaskId = str


class ExecutionPriority(IntEnum):
    BACKGROUND = 0
    INTERACTIVE = 10
