from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from lila.core.types import NodeId

NodeType = Literal["tool", "workflow"]


class _NodeBase(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    id: NodeId = Field(description="A ID for the node unique to the graph this node belongs to.")


class ToolNode(_NodeBase):
    type: Literal["tool"] = "tool"


class WorkflowNode(_NodeBase):
    type: Literal["workflow"] = "workflow"


Node = Annotated[ToolNode | WorkflowNode, Field(discriminator="type")]
