from datetime import datetime

from sqlalchemy import JSON, DateTime
from sqlalchemy import func as f
from sqlalchemy.orm import Mapped, deferred, mapped_column

from lila.core.engine.store.tables.base import Base


class GraphSnapshotSchema(Base):
    __tablename__ = "graph_snapshots"

    hash: Mapped[str] = mapped_column(primary_key=True)
    # deferred - not loaded unless accessed
    # has a 1GB limit in SQLite, which should be enough?
    content: Mapped[JSON] = deferred(mapped_column(JSON))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=f.now(),
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=f.now(),
        onupdate=f.now(),
        index=True,
    )
