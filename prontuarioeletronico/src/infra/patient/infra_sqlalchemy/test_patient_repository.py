"""
Testes unitários para PatientRepository (infra)
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prontuarioeletronico.src.infra.infra_sqlalchemy.base import Base
from .patient_model import PatientModel
from .patient_repository import PatientRepository
from prontuarioeletronico.src.infra.patient.infra_sqlalchemy.patient_model import PatientModel
from prontuarioeletronico.src.domain.patient.patient_entity import Patient
from prontuarioeletronico.src.infra.professional.infra_sqlalchemy.professional_model import ProfessionalModel
import uuid
from datetime import datetime

@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def make_patient():
    return Patient(
        id=str(uuid.uuid4()),
        name="Paciente Teste",
        date_of_birth=datetime(1990, 1, 1),
        gender="M",
        cpf="12345678900",
        email="paciente@teste.com",
        phone="11999999999",
        address="Rua Teste",
        city="Cidade",
        state="Estado",
        insurance="Plano",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

def test_add_and_find_by_id(db_session):
    repo = PatientRepository(db_session)
    patient = make_patient()
    repo.add(patient)
    found = repo.find_by_id(patient.id)
    assert found is not None
    assert found.cpf == patient.cpf

def test_update(db_session):
    repo = PatientRepository(db_session)
    patient = make_patient()
    repo.add(patient)
    updated_patient = Patient(
        id=patient.id,
        name="Paciente Atualizado",
        date_of_birth=patient.date_of_birth,
        gender=patient.gender,
        cpf=patient.cpf,
        email=patient.email,
        phone=patient.phone,
        address=patient.address,
        city=patient.city,
        state=patient.state,
        insurance=patient.insurance,
        created_at=patient.created_at,
        updated_at=datetime.now()
    )
    repo.update(updated_patient)
    found = repo.find_by_id(patient.id)
    assert found.name == "Paciente Atualizado"

def test_delete(db_session):
    repo = PatientRepository(db_session)
    patient = make_patient()
    repo.add(patient)
    repo.delete(patient.id)
    found = repo.find_by_id(patient.id)
    assert found is None
