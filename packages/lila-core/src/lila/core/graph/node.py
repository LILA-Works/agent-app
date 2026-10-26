from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from lila.core.graph.types import NodeId

NodeType = Literal["tool", "workflow"]
RESERVED_IDS = frozenset(
    {
        "nodes",  # $.nodes[-1] would allow indexing the last step, so "nodes" cannot be a node name
    }
)


class _NodeBase(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: NodeId = Field(description="A ID for the node unique to the graph this node belongs to.")

    @field_validator("id")
    @classmethod
    def check_id_not_reserved(cls, value: NodeId) -> NodeId:
        if value in RESERVED_IDS:
            raise ValueError(f"{value!r} is a reserved node ID")
        return value


class ToolNode(_NodeBase):
    type: Literal["tool"] = "tool"


class WorkflowNode(_NodeBase):
    type: Literal["workflow"] = "workflow"


Node = Annotated[ToolNode | WorkflowNode, Field(discriminator="type")]
