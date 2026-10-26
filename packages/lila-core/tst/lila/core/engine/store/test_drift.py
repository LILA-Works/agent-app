from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext

from lila.core.engine.store.tables.base import Base


async def test_migrations__should_match_models(migrated_engine):
    # act
    async with migrated_engine.connect() as conn:
        diff = await conn.run_sync(
            lambda c: compare_metadata(MigrationContext.configure(c), Base.metadata)
        )

    # verify
    assert diff == []
