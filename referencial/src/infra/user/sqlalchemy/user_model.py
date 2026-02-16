from sqlalchemy import Column, String
from infra.api.database import Base
from sqlalchemy.dialects.postgresql import UUID


class UserModel(Base):
    __tablename__ = "tb_users"

    id = Column(UUID, primary_key=True, index=True)
    name = Column(String)
