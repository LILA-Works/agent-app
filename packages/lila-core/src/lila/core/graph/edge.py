from lila.core.types import NodeId
from pydantic import BaseModel, ConfigDict, Field


class Edge(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    source: NodeId = Field(description="The source this directed edge is pointing from.")
    target: NodeId = Field(description="The target this directed edge is pointing to.")
