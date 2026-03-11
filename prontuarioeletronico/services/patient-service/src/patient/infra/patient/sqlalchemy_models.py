from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .sqlalchemy_base import Base


class PatientModel(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), nullable=False, unique=True, index=True)
    date_of_birth: Mapped[str] = mapped_column(String(32), nullable=False)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)


class ConsentModel(Base):
    __tablename__ = "patient_consents"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    legal_basis: Mapped[str] = mapped_column(String(64), nullable=False)
    purpose: Mapped[str] = mapped_column(String(800), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    granted_at: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    revoked_at: Mapped[str | None] = mapped_column(String(64), nullable=True)