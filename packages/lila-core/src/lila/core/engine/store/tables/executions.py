from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy import func as f
from sqlalchemy.orm import Mapped, mapped_column, relationship

from lila.core.engine.store.tables.base import Base
from lila.core.engine.store.tables.graph_snapshots import GraphSnapshotSchema
from lila.core.engine.types import ExecutionId


class ExecutionSchema(Base):
    __tablename__ = "executions"

    id: Mapped[ExecutionId] = mapped_column(primary_key=True)

    graph_hash: Mapped[str] = mapped_column(ForeignKey("graph_snapshots.hash"), index=True)
    graph: Mapped[GraphSnapshotSchema] = relationship()

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

    # optimistic lock
    row_version: Mapped[int] = mapped_column(default=1)
