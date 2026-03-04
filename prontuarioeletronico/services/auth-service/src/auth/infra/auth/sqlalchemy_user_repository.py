from typing import Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from ...domain.auth.role import Role
from ...domain.auth.user_entity import User
from ...domain.auth.user_repository_interface import UserRepositoryInterface
from .sqlalchemy_models import UserModel


class SqlAlchemyUserRepository(UserRepositoryInterface):
    def __init__(self, session: Session):
        self._session = session

    def add(self, entity: User) -> None:
        self._session.add(self._to_model(entity))
        self._session.commit()

    def update(self, entity: User) -> None:
        model = self._session.get(UserModel, entity.id)
        if model is None:
            raise ValueError("user not found")

        model.username = entity.username
        model.password_hash = entity.password_hash
        model.role = entity.role.value
        model.active = entity.active
        self._session.commit()

    def delete(self, id: str) -> None:
        model = self._session.get(UserModel, id)
        if model:
            self._session.delete(model)
            self._session.commit()

    def find_by_id(self, id: str) -> Optional[User]:
        model = self._session.get(UserModel, id)
        return self._to_entity(model)

    def find_all(self) -> list[User]:
        models = self._session.query(UserModel).all()
        return [self._to_entity(model) for model in models if model is not None]

    def find_by_username(self, username: str) -> Optional[User]:
        model = (
            self._session.query(UserModel)
            .filter(func.lower(UserModel.username) == username.strip().lower())
            .one_or_none()
        )
        return self._to_entity(model)

    @staticmethod
    def _to_entity(model: UserModel | None) -> Optional[User]:
        if model is None:
            return None

        role = Role(model.role)
        return User(
            id=model.id,
            username=model.username,
            password_hash=model.password_hash,
            role=role,
            active=model.active,
        )

    @staticmethod
    def _to_model(entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            username=entity.username,
            password_hash=entity.password_hash,
            role=entity.role.value,
            active=entity.active,
        )
