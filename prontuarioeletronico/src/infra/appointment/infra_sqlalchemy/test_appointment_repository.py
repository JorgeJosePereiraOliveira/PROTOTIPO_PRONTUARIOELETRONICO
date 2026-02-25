"""
Testes unitários para AppointmentRepository (infra)
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prontuarioeletronico.src.infra.infra_sqlalchemy.base import Base
from .appointment_model import AppointmentModel
from .appointment_repository import AppointmentRepository
from prontuarioeletronico.src.infra.appointment.infra_sqlalchemy.appointment_model import AppointmentModel
from prontuarioeletronico.src.domain.appointment.appointment_entity import Appointment
from prontuarioeletronico.src.infra.patient.infra_sqlalchemy.patient_model import PatientModel
from prontuarioeletronico.src.infra.professional.infra_sqlalchemy.professional_model import ProfessionalModel
import uuid
from datetime import datetime

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    # Importa todos os modelos necessários para ForeignKey
    # (os imports acima já garantem o registro das tabelas)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def make_appointment():
    return Appointment(
        id=str(uuid.uuid4()),
        patient_id="patient-1",
        professional_id="prof-1",
        appointment_date=datetime.now(),
        reason="Consulta de rotina",
        status="scheduled",
        notes=None,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

def test_save_and_find_by_id(db_session):
    repo = AppointmentRepository(db_session)
    appt = make_appointment()
    repo.add(appt)
    found = repo.find_by_id(appt.id)
    assert found is not None
    assert found.status == appt.status

def test_update(db_session):
    repo = AppointmentRepository(db_session)
    appt = make_appointment()
    repo.add(appt)
    appt.mark_completed()
    repo.update(appt)
    found = repo.find_by_id(appt.id)
    assert found.status == "completed"

def test_delete(db_session):
    repo = AppointmentRepository(db_session)
    appt = make_appointment()
    repo.add(appt)
    repo.delete(appt.id)
    found = repo.find_by_id(appt.id)
    assert found is None
