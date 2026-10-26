from pathlib import Path

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from lila.core.engine.base import Engine
from lila.core.engine.store.migrate import upgrade
from lila.core.engine.store.sqlite import SqliteStore, create_engine
from lila.core.engine.store.tables import ExecutionSchema
from lila.core.graph.loader import from_yaml

CORE_DIR = Path(__file__).parent.parent
HELLO_WORLD_PATH = (
    CORE_DIR
    / "test-data"
    / "test_home"
    / "toolkits"
    / "namespace"
    / "workflows"
    / "hello_world.yaml"
)


# region fixture
@pytest.fixture
async def db_engine(tmp_path: Path):
    engine = create_engine(str(tmp_path / "integ.db"))
    async with engine.begin() as conn:
        await conn.run_sync(upgrade)
    yield engine
    await engine.dispose()


@pytest.fixture
def engine(db_engine: AsyncEngine) -> Engine:
    return Engine(store=SqliteStore(engine=db_engine))


# endregion fixture


async def test_engine__process_job_successfully(engine: Engine, db_engine: AsyncEngine):
    # prepare
    graph = from_yaml(HELLO_WORLD_PATH)
    inputs = {"some_number": 1, "some_string": "a"}

    # act
    # TODO: only submit exists so far, extend as the engine gains the rest of the job lifecycle.
    execution_id = await engine.submit(inputs=inputs, graph=graph)

    # verify
    async with AsyncSession(db_engine) as session:
        execution = await session.scalar(
            select(ExecutionSchema).where(ExecutionSchema.id == execution_id)
        )
    assert execution is not None
    assert execution.graph_hash == graph.hash()
    assert execution.inputs == inputs
