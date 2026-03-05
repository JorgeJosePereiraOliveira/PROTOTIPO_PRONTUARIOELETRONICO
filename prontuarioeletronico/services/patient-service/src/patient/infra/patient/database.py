import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .sqlalchemy_base import Base


DATABASE_URL = os.getenv("PATIENT_DATABASE_URL", "sqlite:///./patient.db")

_engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **_engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_database() -> None:
    Base.metadata.create_all(bind=engine)