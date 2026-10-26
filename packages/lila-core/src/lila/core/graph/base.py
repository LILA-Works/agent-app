from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, model_validator

from lila.core.graph.edge import Edge
from lila.core.graph.node import Node
from lila.core.graph.types import JsonSchema, LogPath, NodeId


class Graph(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    # composition
    entry: NodeId = Field(
        description="The starting node for this graph. Each graph has only one starting node."
    )
    nodes: tuple[Node, ...] = Field(description="The list of nodes that are in this graph.")
    edges: tuple[Edge, ...] | None = Field(description="The list of edges that are in this graph.")

    # boundaries
    input_schema: JsonSchema
    output_schema: JsonSchema
    output: dict[str, LogPath]

    # metadata
    description: str = ""  #  what this graph does.
    source: Path | None = None

    # region: validation
    @model_validator(mode="after")
    def check_unique_node_ids(self) -> "Graph":
        ids = [n.id for n in self.nodes]
        duplicates = sorted({i for i in ids if ids.count(i) > 1})
        if duplicates:
            raise ValueError(f"duplicate node IDs found: {duplicates}")
        return self

    @model_validator(mode="after")
    def check_entry_exists(self) -> "Graph":
        if self.entry not in {n.id for n in self.nodes}:
            raise ValueError(
                f"entry {self.entry!r} is not a node ID that points " "to any nodes in this graph"
            )
        return self

    @model_validator(mode="after")
    def check_edges_reference_nodes(self) -> "Graph":
        if not self.edges:  # if only one node
            return self

        ids = {n.id for n in self.nodes}
        bad = [
            (e.source, e.target) for e in self.edges if e.source not in ids or e.target not in ids
        ]
        if bad:
            raise ValueError(f"edges reference unknown nodes: {bad}")
        return self

    # endregion: validation
