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
        _ensure_legacy_columns()


def _ensure_legacy_columns() -> None:
    with engine.begin() as connection:
        inspector = inspect(connection)
        table_names = set(inspector.get_table_names())

        if "problems" in table_names:
            problem_columns = {
                column["name"] for column in inspector.get_columns("problems")
            }
            if "terminology_system" not in problem_columns:
                connection.execute(
                    text(
                        "ALTER TABLE problems ADD COLUMN terminology_system VARCHAR(32) NOT NULL DEFAULT 'cid'"
                    )
                )
            if "terminology_code" not in problem_columns:
                connection.execute(
                    text(
                        "ALTER TABLE problems ADD COLUMN terminology_code VARCHAR(64) NOT NULL DEFAULT 'I10'"
                    )
                )
            if "created_at" not in problem_columns:
                connection.execute(
                    text(
                        "ALTER TABLE problems ADD COLUMN created_at VARCHAR(64) NOT NULL DEFAULT '1970-01-01T00:00:00Z'"
                    )
                )

        if "soap_records" in table_names:
            soap_columns = {
                column["name"] for column in inspector.get_columns("soap_records")
            }
            if "created_at" not in soap_columns:
                connection.execute(
                    text(
                        "ALTER TABLE soap_records ADD COLUMN created_at VARCHAR(64) NOT NULL DEFAULT '1970-01-01T00:00:00Z'"
                    )
                )
