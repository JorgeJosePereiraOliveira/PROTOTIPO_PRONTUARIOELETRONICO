"""
SQLAlchemy Repository Implementation for Clinical Record
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ....domain.clinical_record.rcop_soap import (
    ClinicalRecord, Subjective, Objective, Assessment, Plan, Problem
)
from ....domain.__seedwork.repository_interface import RepositoryInterface
from .clinical_record_model import (
    ClinicalRecordModel, ProblemModel, SubjectiveModel, ObjectiveModel,
    AssessmentModel, PlanModel
)


class ClinicalRecordRepository(RepositoryInterface[ClinicalRecord]):
    """Repository implementation for Clinical Record persistence"""
    
    def __init__(self, db: Session):
        self._db = db
    
    def add(self, entity: ClinicalRecord) -> None:
        """Add a new clinical record"""
        record_model = ClinicalRecordModel(
            id=entity.id,
            patient_id=entity.patient_id,
            professional_id=entity.professional_id,
            problem_id=entity.problem_id,
            encounter_date=entity.encounter_date
        )
        self._db.add(record_model)
        
        # Add SOAP components
        if entity.subjective:
            subj_model = SubjectiveModel(
                id=entity.subjective.id,
                clinical_record_id=entity.id,
                patient_complaint=entity.subjective.patient_complaint,
                medical_history=entity.subjective.medical_history,
                medications=entity.subjective.medications,
                allergies=entity.subjective.allergies
            )
            self._db.add(subj_model)
        
        if entity.objective:
            obj_model = ObjectiveModel(
                id=entity.objective.id,
                clinical_record_id=entity.id,
                vital_signs=entity.objective.vital_signs,
                physical_examination=entity.objective.physical_examination,
                lab_results=entity.objective.lab_results
            )
            self._db.add(obj_model)
        
        if entity.assessment:
            assess_model = AssessmentModel(
                id=entity.assessment.id,
                clinical_record_id=entity.id,
                diagnosis=entity.assessment.diagnosis,
                clinical_impression=entity.assessment.clinical_impression,
                differential_diagnoses=entity.assessment.differential_diagnoses
            )
            self._db.add(assess_model)
        
        if entity.plan:
            plan_model = PlanModel(
                id=entity.plan.id,
                clinical_record_id=entity.id,
                treatment_plan=entity.plan.treatment_plan,
                medications=entity.plan.medications,
                procedures=entity.plan.procedures,
                follow_up=entity.plan.follow_up
            )
            self._db.add(plan_model)
        
        self._db.commit()
    
    def update(self, entity: ClinicalRecord) -> None:
        """Update a clinical record"""
        record_model = self._db.query(ClinicalRecordModel).filter(
            ClinicalRecordModel.id == entity.id
        ).first()
        if not record_model:
            raise ValueError(f"Clinical Record {entity.id} not found")
        
        record_model.updated_at = datetime.now()
        self._db.commit()
    
    def delete(self, id: str) -> None:
        """Delete a clinical record"""
        record_model = self._db.query(ClinicalRecordModel).filter(
            ClinicalRecordModel.id == id
        ).first()
        if not record_model:
            raise ValueError(f"Clinical Record {id} not found")
        
        self._db.delete(record_model)
        self._db.commit()
    
    def find_by_id(self, id: str) -> Optional[ClinicalRecord]:
        """Find a clinical record by ID"""
        record_model = self._db.query(ClinicalRecordModel).filter(
            ClinicalRecordModel.id == id
        ).first()
        if not record_model:
            return None
        return self._to_domain(record_model)
    
    def find_all(self) -> List[ClinicalRecord]:
        """Find all clinical records"""
        models = self._db.query(ClinicalRecordModel).all()
        return [self._to_domain(m) for m in models]
    
    def find_problem_by_id(self, id: str) -> Optional[Problem]:
        """Find a problem by ID"""
        problem_model = self._db.query(ProblemModel).filter(
            ProblemModel.id == id
        ).first()
        if not problem_model:
            return None
        return self._problem_to_domain(problem_model)
    
    def add_problem(self, entity: Problem) -> None:
        """Add a new problem"""
        problem_model = ProblemModel(
            id=entity.id,
            patient_id=entity.patient_id,
            description=entity.description,
            icd10_code=entity.icd10_code,
            status=entity.status
        )
        self._db.add(problem_model)
        self._db.commit()
    
    def _to_domain(self, model: ClinicalRecordModel) -> ClinicalRecord:
        """Convert SQLAlchemy model to domain entity"""
        # Load SOAP components
        subj_model = self._db.query(SubjectiveModel).filter(
            SubjectiveModel.clinical_record_id == model.id
        ).first()
        subjective = None
        if subj_model:
            subjective = self._subjective_to_domain(subj_model)
        
        obj_model = self._db.query(ObjectiveModel).filter(
            ObjectiveModel.clinical_record_id == model.id
        ).first()
        objective = None
        if obj_model:
            objective = self._objective_to_domain(obj_model)
        
        assess_model = self._db.query(AssessmentModel).filter(
            AssessmentModel.clinical_record_id == model.id
        ).first()
        assessment = None
        if assess_model:
            assessment = self._assessment_to_domain(assess_model)
        
        plan_model = self._db.query(PlanModel).filter(
            PlanModel.clinical_record_id == model.id
        ).first()
        plan = None
        if plan_model:
            plan = self._plan_to_domain(plan_model)
        
        return ClinicalRecord(
            id=model.id,
            patient_id=model.patient_id,
            professional_id=model.professional_id,
            problem_id=model.problem_id,
            encounter_date=model.encounter_date,
            subjective=subjective,
            objective=objective,
            assessment=assessment,
            plan=plan,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _subjective_to_domain(self, model: SubjectiveModel) -> Subjective:
        return Subjective(
            id=model.id,
            clinical_record_id=model.clinical_record_id,
            patient_complaint=model.patient_complaint,
            medical_history=model.medical_history,
            medications=model.medications,
            allergies=model.allergies,
            created_at=model.created_at
        )
    
    def _objective_to_domain(self, model: ObjectiveModel) -> Objective:
        return Objective(
            id=model.id,
            clinical_record_id=model.clinical_record_id,
            vital_signs=model.vital_signs,
            physical_examination=model.physical_examination,
            lab_results=model.lab_results,
            imaging_results=model.imaging_results,
            created_at=model.created_at
        )
    
    def _assessment_to_domain(self, model: AssessmentModel) -> Assessment:
        return Assessment(
            id=model.id,
            clinical_record_id=model.clinical_record_id,
            diagnosis=model.diagnosis,
            clinical_impression=model.clinical_impression,
            differential_diagnoses=model.differential_diagnoses,
            created_at=model.created_at
        )
    
    def _plan_to_domain(self, model: PlanModel) -> Plan:
        return Plan(
            id=model.id,
            clinical_record_id=model.clinical_record_id,
            treatment_plan=model.treatment_plan,
            medications=model.medications,
            procedures=model.procedures,
            follow_up=model.follow_up,
            created_at=model.created_at
        )
    
    def _problem_to_domain(self, model: ProblemModel) -> Problem:
        return Problem(
            id=model.id,
            patient_id=model.patient_id,
            description=model.description,
            icd10_code=model.icd10_code,
            status=model.status,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
