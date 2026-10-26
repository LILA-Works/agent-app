import pytest

from lila.core.engine.store.migrate import upgrade
from lila.core.engine.store.sqlite import create_engine
from lila.core.engine.store.tables.base import Base


@pytest.fixture
async def migrated_engine(tmp_path):
    # slower compared to created_engine that creates all models at once
    # good for e2e test
    engine = create_engine(str(tmp_path / "test.db"))
    async with engine.begin() as conn:
        await conn.run_sync(upgrade)
    yield engine
    await engine.dispose()


@pytest.fixture
async def created_engine(tmp_path):
    # faster, good for unit tests
    engine = create_engine(str(tmp_path / "test.db"))
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()
