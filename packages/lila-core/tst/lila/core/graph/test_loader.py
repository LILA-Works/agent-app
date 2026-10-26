from pathlib import Path

import pytest

from lila.core.graph.errors import ParseError
from lila.core.graph.loader import from_yaml

TST_DIR = Path(__file__).parent.parent.parent.parent
UNIT_TEST_DATA_DIR = Path(__file__).parent / "data"
E2E_TEST_HOME_DIR = TST_DIR / "data" / "test_home"


# region: fixtures
@pytest.fixture
def minimal_graph_path() -> Path:
    """Two nodes (`a` -> `b`) joined by one edge."""
    return UNIT_TEST_DATA_DIR / "minimal_graph.yaml"


@pytest.fixture
def hello_world_graph_path() -> Path:
    return E2E_TEST_HOME_DIR / "toolkits" / "namespace" / "workflows" / "hello_world.yaml"


# endregion: fixtures


# region: test cases
def test_from_yaml__fails_on_empty_file(tmp_path):
    # prepare
    yaml_path = tmp_path / "graph.yaml"
    yaml_path.write_text("")

    # act
    with pytest.raises(ParseError) as exc_info:
        from_yaml(yaml_path)

    # verify
    assert "top level must be a mapping" in str(exc_info.value)
    assert "NoneType" in str(exc_info.value)


def test_from_yaml__fails_on_top_level_string_value(tmp_path):
    # prepare
    yaml_path = tmp_path / "graph.yaml"
    yaml_path.write_text("just a string")

    # act
    with pytest.raises(ParseError) as exc_info:
        from_yaml(yaml_path)

    # verify
    assert "top level must be a mapping" in str(exc_info.value)
    assert "str" in str(exc_info.value)


def test_from_yaml__succeeds_loading_minimal_graph(minimal_graph_path):
    # act
    graph = from_yaml(minimal_graph_path)

    # verify
    assert graph.entry == "a"
    assert [n.id for n in graph.nodes] == ["a", "b"]
    assert graph.edges and len(graph.edges) > 0
    assert [(e.source, e.target) for e in graph.edges] == [("a", "b")]
    assert graph.source == minimal_graph_path


def test_from_yaml__succeeds_loading_hello_world_graph(hello_world_graph_path):
    # act
    graph = from_yaml(hello_world_graph_path)

    # verify
    assert graph.entry == "check_time"
    assert graph.source == hello_world_graph_path


# endregion: test cases
