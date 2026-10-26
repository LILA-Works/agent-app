from sqlalchemy import URL, event
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine


def create_engine(path: str) -> AsyncEngine:
    engine = create_async_engine(URL.create("sqlite+aiosqlite", database=path))

    @event.listens_for(engine.sync_engine, "connect")
    def _enable_foreign_keys(dbapi_conn, _):
        # sqlite doesn't enforce foreign keys by default, needs to be set per connection.
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

    return engine


class SqliteStore:
    def __init__(self, engine: AsyncEngine):
        self._session = async_sessionmaker(engine, expire_on_commit=False)
