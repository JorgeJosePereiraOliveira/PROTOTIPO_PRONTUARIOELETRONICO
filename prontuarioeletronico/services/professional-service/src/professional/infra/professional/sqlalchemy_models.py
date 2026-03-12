from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .sqlalchemy_base import Base


class ProfessionalModel(Base):
    __tablename__ = "professionals"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    full_name: Mapped[str] = mapped_column(String(160), nullable=False)
    document_cpf: Mapped[str] = mapped_column(String(11), nullable=False, index=True)
    council_type: Mapped[str] = mapped_column(String(16), nullable=False, index=True)
    council_uf: Mapped[str] = mapped_column(String(2), nullable=False, index=True)
    council_number: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    occupation: Mapped[str] = mapped_column(String(80), nullable=False)
    specialty: Mapped[str | None] = mapped_column(String(120), nullable=True)
    auth_user_id: Mapped[str | None] = mapped_column(String(64), nullable=True, index=True)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    created_at: Mapped[str] = mapped_column(String(64), nullable=False)
    updated_at: Mapped[str] = mapped_column(String(64), nullable=False)
