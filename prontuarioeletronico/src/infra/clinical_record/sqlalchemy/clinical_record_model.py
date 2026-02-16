"""
SQLAlchemy Model for Clinical Record (RCOP/SOAP)
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class ClinicalRecordModel(Base):
    """SQLAlchemy ORM model for Clinical Record persistence"""
    __tablename__ = "clinical_records"
    
    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    professional_id = Column(String, ForeignKey("professionals.id"), nullable=False)
    problem_id = Column(String, nullable=False)
    encounter_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class ProblemModel(Base):
    """SQLAlchemy ORM model for clinical problems"""
    __tablename__ = "problems"
    
    id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.id"), nullable=False)
    description = Column(String, nullable=False)
    icd10_code = Column(String, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


class SubjectiveModel(Base):
    """SQLAlchemy ORM model for SOAP Subjective component"""
    __tablename__ = "soap_subjectives"
    
    id = Column(String, primary_key=True, index=True)
    clinical_record_id = Column(String, ForeignKey("clinical_records.id"), nullable=False)
    patient_complaint = Column(Text, nullable=False)
    medical_history = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    allergies = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class ObjectiveModel(Base):
    """SQLAlchemy ORM model for SOAP Objective component"""
    __tablename__ = "soap_objectives"
    
    id = Column(String, primary_key=True, index=True)
    clinical_record_id = Column(String, ForeignKey("clinical_records.id"), nullable=False)
    vital_signs = Column(Text, nullable=False)
    physical_examination = Column(Text, nullable=False)
    lab_results = Column(Text, nullable=True)
    imaging_results = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class AssessmentModel(Base):
    """SQLAlchemy ORM model for SOAP Assessment component"""
    __tablename__ = "soap_assessments"
    
    id = Column(String, primary_key=True, index=True)
    clinical_record_id = Column(String, ForeignKey("clinical_records.id"), nullable=False)
    diagnosis = Column(Text, nullable=False)
    clinical_impression = Column(Text, nullable=False)
    differential_diagnoses = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class PlanModel(Base):
    """SQLAlchemy ORM model for SOAP Plan component"""
    __tablename__ = "soap_plans"
    
    id = Column(String, primary_key=True, index=True)
    clinical_record_id = Column(String, ForeignKey("clinical_records.id"), nullable=False)
    treatment_plan = Column(Text, nullable=False)
    medications = Column(Text, nullable=True)
    procedures = Column(Text, nullable=True)
    follow_up = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
