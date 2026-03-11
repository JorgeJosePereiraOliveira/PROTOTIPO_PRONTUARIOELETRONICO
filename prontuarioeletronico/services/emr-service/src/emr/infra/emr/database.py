import os

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from .sqlalchemy_base import Base


APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_URL = os.getenv("EMR_DATABASE_URL", "sqlite:///./emr.db")

if APP_ENV in {"production", "staging"} and "EMR_DATABASE_URL" not in os.environ:
    raise RuntimeError("EMR_DATABASE_URL is required for production/staging")

_engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **_engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
    if DATABASE_URL.startswith("sqlite"):
        _ensure_problem_terminology_columns()


def _ensure_problem_terminology_columns() -> None:
    with engine.begin() as connection:
        inspector = inspect(connection)
        if "problems" not in inspector.get_table_names():
            return

        existing_columns = {column["name"] for column in inspector.get_columns("problems")}

        if "terminology_system" not in existing_columns:
            connection.execute(
                text(
                    "ALTER TABLE problems ADD COLUMN terminology_system VARCHAR(32) NOT NULL DEFAULT 'cid'"
                )
            )
        if "terminology_code" not in existing_columns:
            connection.execute(
                text(
                    "ALTER TABLE problems ADD COLUMN terminology_code VARCHAR(64) NOT NULL DEFAULT 'I10'"
                )
            )
