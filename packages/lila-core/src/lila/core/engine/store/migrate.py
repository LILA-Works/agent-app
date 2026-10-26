from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import Connection

MIGRATIONS_DIR = Path(__file__).parent / "migrations"


def upgrade(connection: Connection, revision: str = "head") -> None:
    cfg = Config()
    cfg.set_main_option("script_location", str(MIGRATIONS_DIR))
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, revision)
