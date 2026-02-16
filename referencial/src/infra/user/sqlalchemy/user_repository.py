from typing import List
from uuid import UUID
from domain.user.user_entity import User
from domain.user.user_repository_interface import UserRepositoryInterface
from sqlalchemy.orm.session import Session

from infra.user.sqlalchemy.user_model import UserModel


class UserRepository(UserRepositoryInterface):

    def __init__(self, session: Session):
        self.session: Session = session

    def add_user(self, user: User) -> None:

        user_model = UserModel(id=user.id, name=user.name)

        self.session.add(user_model)
        self.session.commit()

        return None

    def find_user(self, user_id: UUID) -> User:

        user_in_db: UserModel = self.session.query(UserModel).get(user_id)
        user = User(id=user_in_db.id, name=user_in_db.name)

        return user

    def list_users(self) -> List[User]:

        users_in_db = self.session.query(UserModel).all()

        users = []

        for user_in_db in users_in_db:
            users.append(User(id=user_in_db.id, name=user_in_db.name))

        return users

    def update_user(self, user: User) -> None:

        self.session.query(UserModel).filter(UserModel.id == user.id).update(
            {"name": user.name}
        )
        self.session.commit()

        return None
