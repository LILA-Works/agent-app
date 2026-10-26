from uuid import uuid4

from pydantic import JsonValue
from sqlalchemy import URL, event
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from lila.core.engine.store.tables import ExecutionSchema, GraphSnapshotSchema
from lila.core.engine.types import ExecutionId
from lila.core.graph.base import Graph


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

    async def create_execution(self, inputs: JsonValue, graph: Graph) -> ExecutionId:
        graph_hash = graph.hash()
        execution_id = uuid4().hex

        async with self._session.begin() as session:
            # snapshots are content-addressed, so an existing hash is already correct.
            await session.execute(
                insert(GraphSnapshotSchema)
                .values(hash=graph_hash, content=graph.model_dump(mode="json"))
                .on_conflict_do_nothing(index_elements=["hash"])
            )
            session.add(ExecutionSchema(id=execution_id, graph_hash=graph_hash, inputs=inputs))

        return execution_id
