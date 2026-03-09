from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .sqlalchemy_base import Base


class ProblemModel(Base):
    __tablename__ = "problems"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(800), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)


class SOAPRecordModel(Base):
    __tablename__ = "soap_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    problem_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("problems.id"),
        nullable=False,
        index=True,
    )
    patient_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    professional_id: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    subjective: Mapped[str] = mapped_column(String(2000), nullable=False)
    objective: Mapped[str] = mapped_column(String(2000), nullable=False)
    assessment: Mapped[str] = mapped_column(String(2000), nullable=False)
    plan: Mapped[str] = mapped_column(String(2000), nullable=False)
