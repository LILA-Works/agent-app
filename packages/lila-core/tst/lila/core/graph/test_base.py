import pytest
from lila.core.graph.base import Graph
from lila.core.graph.edge import Edge
from lila.core.graph.node import ToolNode
from lila.core.types import JsonSchema
from pydantic import ValidationError


# region: test cases
class TestGraph:
    def test_check_unique_node_id__fails_if_duplicate_ids(self):
        # act
        with pytest.raises(ValidationError) as exc_info:
            Graph(
                entry="a",
                nodes=(ToolNode(id="a"), ToolNode(id="a")),
                edges=(),
                input_schema=JsonSchema(type="object"),
                output_schema=JsonSchema(type="object"),
                output={"result": "$.a.result"},
            )

        # verify
        assert "duplicate node IDs found: ['a']" in str(exc_info.value)

    def test_check_entry_exists__fails_if_entry_not_in_nodes(self):
        # act
        with pytest.raises(ValidationError) as exc_info:
            Graph(
                entry="missing",
                nodes=(ToolNode(id="a"),),
                edges=(),
                input_schema=JsonSchema(type="object"),
                output_schema=JsonSchema(type="object"),
                output={"result": "$.a.result"},
            )

        # verify
        assert "entry 'missing' is not a node ID" in str(exc_info.value)

    @pytest.mark.parametrize(
        "edge",
        [
            Edge(source="a", target="missing"),
            Edge(source="missing", target="a"),
        ],
        ids=["unknown_target", "unknown_source"],
    )
    def test_check_edges_reference_nodes__fails_if_edge_has_unknown_node(self, edge):
        # act
        with pytest.raises(ValidationError) as exc_info:
            Graph(
                entry="a",
                nodes=(ToolNode(id="a"),),
                edges=(edge,),
                input_schema=JsonSchema(type="object"),
                output_schema=JsonSchema(type="object"),
                output={"result": "$.a.result"},
            )

        # verify
        assert "edges reference unknown nodes" in str(exc_info.value)
        assert "missing" in str(exc_info.value)


# endregion: test cases
