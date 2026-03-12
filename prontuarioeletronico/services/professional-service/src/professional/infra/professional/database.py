import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .sqlalchemy_base import Base


APP_ENV = os.getenv("APP_ENV", "development")
DATABASE_URL = os.getenv("PROFESSIONAL_DATABASE_URL", "sqlite:///./professional.db")

if APP_ENV in {"production", "staging"} and "PROFESSIONAL_DATABASE_URL" not in os.environ:
    raise RuntimeError("PROFESSIONAL_DATABASE_URL is required for production/staging")

_engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **_engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_database() -> None:
    Base.metadata.create_all(bind=engine)
