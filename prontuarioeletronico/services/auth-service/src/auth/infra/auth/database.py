import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .sqlalchemy_base import Base
from .sqlalchemy_models import UserModel
from .bcrypt_password_hasher import BcryptPasswordHasher


DATABASE_URL = os.getenv("AUTH_DATABASE_URL", "sqlite:///./auth.db")

_engine_kwargs = {}
if DATABASE_URL.startswith("sqlite"):
    _engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **_engine_kwargs)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_database() -> None:
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        existing_count = session.query(UserModel).count()
        if existing_count == 0:
            hasher = BcryptPasswordHasher()
            session.add_all(
                [
                    UserModel(
                        id="u-admin",
                        username="admin",
                        password_hash=hasher.hash("admin123"),
                        role="admin",
                        active=True,
                    ),
                    UserModel(
                        id="u-prof",
                        username="profissional",
                        password_hash=hasher.hash("prof123"),
                        role="profissional",
                        active=True,
                    ),
                ]
            )
            session.commit()
    finally:
        session.close()
