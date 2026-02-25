"""
Testes unitários para ClinicalRecordRepository (infra)
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from prontuarioeletronico.src.infra.infra_sqlalchemy.base import Base
from .clinical_record_model import ClinicalRecordModel
from .clinical_record_repository import ClinicalRecordRepository
from prontuarioeletronico.src.infra.clinical_record.infra_sqlalchemy.clinical_record_model import ClinicalRecordModel
from prontuarioeletronico.src.domain.clinical_record.rcop_soap import ClinicalRecord
import uuid
from datetime import datetime
from prontuarioeletronico.src.infra.patient.infra_sqlalchemy.patient_model import PatientModel
from prontuarioeletronico.src.infra.professional.infra_sqlalchemy.professional_model import ProfessionalModel

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


def make_clinical_record():
    return ClinicalRecord(
        id=str(uuid.uuid4()),
        patient_id="patient-1",
        professional_id="prof-1",
        problem_id="prob-1",
        encounter_date=datetime.now(),
        subjective=None,
        objective=None,
        assessment=None,
        plan=None,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

def test_add_and_find_by_id(db_session):
    repo = ClinicalRecordRepository(db_session)
    rec = make_clinical_record()
    repo.add(rec)
    found = repo.find_by_id(rec.id)
    assert found is not None
    assert found.patient_id == rec.patient_id

def test_update(db_session):
    repo = ClinicalRecordRepository(db_session)
    rec = make_clinical_record()
    repo.add(rec)
    updated_rec = ClinicalRecord(
        id=rec.id,
        patient_id=rec.patient_id,
        professional_id=rec.professional_id,
        problem_id="prob-2",
        encounter_date=rec.encounter_date,
        subjective=rec.subjective,
        objective=rec.objective,
        assessment=rec.assessment,
        plan=rec.plan,
        created_at=rec.created_at,
        updated_at=datetime.now()
    )
    repo.update(updated_rec)
    found = repo.find_by_id(rec.id)
    assert found.problem_id == "prob-2"

def test_delete(db_session):
    repo = ClinicalRecordRepository(db_session)
    rec = make_clinical_record()
    repo.add(rec)
    repo.delete(rec.id)
    found = repo.find_by_id(rec.id)
    assert found is None
