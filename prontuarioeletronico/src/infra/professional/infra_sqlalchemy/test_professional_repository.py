"""
Testes unitários para ProfessionalRepository (infra)
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prontuarioeletronico.src.infra.infra_sqlalchemy.base import Base
from .professional_model import ProfessionalModel
from .professional_repository import ProfessionalRepository
from prontuarioeletronico.src.infra.professional.infra_sqlalchemy.professional_model import ProfessionalModel
from prontuarioeletronico.src.domain.professional.professional_entity import Professional
from prontuarioeletronico.src.infra.patient.infra_sqlalchemy.patient_model import PatientModel
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


def make_professional():
    return Professional(
        id=str(uuid.uuid4()),
        name="Dr. Teste",
        license_number="12345",
        specialties=["Cardiologia", "Clínica Geral"],
        crm="CRM1234",
        email="dr@teste.com",
        phone="11999999999",
        institution="Hospital Teste",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

def test_save_and_find_by_id(db_session):
    repo = ProfessionalRepository(db_session)
    prof = make_professional()
    repo.save(prof)
    found = repo.find_by_id(prof.id)
    assert found is not None
    assert found.name == prof.name
    assert set(found.specialties) == set(prof.specialties)

def test_update(db_session):
    repo = ProfessionalRepository(db_session)
    prof = make_professional()
    repo.save(prof)
    updated_prof = Professional(
        id=prof.id,
        name="Dr. Atualizado",
        license_number=prof.license_number,
        specialties=prof.specialties + ["Neurologia"],
        crm=prof.crm,
        email=prof.email,
        phone=prof.phone,
        institution=prof.institution,
        created_at=prof.created_at,
        updated_at=datetime.now()
    )
    repo.update(updated_prof)
    found = repo.find_by_id(prof.id)
    assert found.name == "Dr. Atualizado"
    assert "Neurologia" in found.specialties

def test_delete(db_session):
    repo = ProfessionalRepository(db_session)
    prof = make_professional()
    repo.save(prof)
    repo.delete(prof.id)
    found = repo.find_by_id(prof.id)
    assert found is None
