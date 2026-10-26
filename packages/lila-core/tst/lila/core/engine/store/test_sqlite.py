import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from lila.core.engine.store.sqlite import SqliteStore
from lila.core.engine.store.tables import ExecutionSchema, GraphSnapshotSchema
from lila.core.graph.base import Graph
from lila.core.graph.node import ToolNode
from lila.core.graph.types import JsonSchema


# region fixture
@pytest.fixture
def store(created_engine: AsyncEngine) -> SqliteStore:
    return SqliteStore(engine=created_engine)


@pytest.fixture
def graph() -> Graph:
    return Graph(
        entry="a",
        nodes=(ToolNode(id="a", tool="abc/etc", args={}),),
        edges=(),
        input_schema=JsonSchema(type="object"),
        output_schema=JsonSchema(type="object"),
        output={"result": "$.a.result"},
    )


# endregion fixture


# region create_execution
async def test_create_execution__persists_execution_and_graph_snapshot(
    store: SqliteStore, created_engine: AsyncEngine, graph: Graph
) -> None:
    # act
    execution_id = await store.create_execution({"name": "lila"}, graph)

    # verify
    async with AsyncSession(created_engine) as session:
        execution = await session.get(ExecutionSchema, execution_id)
        snapshot = await session.get(GraphSnapshotSchema, graph.hash())
        # content is deferred, so it has to be loaded while the session is open
        snapshot_content = await session.scalar(
            select(GraphSnapshotSchema.content).where(GraphSnapshotSchema.hash == graph.hash())
        )
    assert execution is not None
    assert execution.inputs == {"name": "lila"}
    assert execution.graph_hash == graph.hash()
    assert snapshot is not None
    assert snapshot_content == graph.model_dump(mode="json")


async def test_create_execution__reuses_snapshot_when_graph_is_same(
    store: SqliteStore, created_engine: AsyncEngine, graph: Graph
) -> None:
    # act
    first_id = await store.create_execution({"n": 1}, graph)
    second_id = await store.create_execution({"n": 2}, graph)

    # verify
    async with AsyncSession(created_engine) as session:
        snapshot_count = await session.scalar(select(func.count()).select_from(GraphSnapshotSchema))
        execution_count = await session.scalar(select(func.count()).select_from(ExecutionSchema))
    assert first_id != second_id
    assert snapshot_count == 1
    assert execution_count == 2


# endregion create_execution
