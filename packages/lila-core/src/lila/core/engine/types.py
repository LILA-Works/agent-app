from enum import IntEnum

type ExecutionId = str

type TaskId = str


# may want this later, not using for now
class ExecutionPriority(IntEnum):
    BACKGROUND = 0
    INTERACTIVE = 10
