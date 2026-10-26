import pytest

from lila.core.engine.store.sqlite import SqliteStore


@pytest.fixture
def store(created_engine):
    return SqliteStore(engine=created_engine)
