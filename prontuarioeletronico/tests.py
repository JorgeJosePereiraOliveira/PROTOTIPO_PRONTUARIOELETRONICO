"""
Unit Tests - Demonstrando testabilidade sem banco de dados ou interfaces
"""

import unittest
from datetime import datetime
from prontuarioeletronico.src.domain.patient.patient_entity import Patient
from prontuarioeletronico.src.domain.clinical_record.rcop_soap import Problem, ClinicalRecord, Subjective, Objective, Assessment, Plan
from prontuarioeletronico.src.domain.appointment.appointment_entity import Appointment


class TestPatientEntity(unittest.TestCase):
    """Tests for Patient entity - demonstrating domain layer testability"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.patient = Patient(
            id="patient-001",
            name="João Silva",
            date_of_birth=datetime(1990, 5, 15),
            gender="M",
            cpf="12345678901",
            email="joao@example.com",
            phone="11999999999"
        )
    
    def test_patient_creation(self):
        """Test patient entity creation"""
        self.assertEqual(self.patient.id, "patient-001")
        self.assertEqual(self.patient.name, "João Silva")
        self.assertEqual(self.patient.cpf, "12345678901")
    
    def test_calculate_age(self):
        """Test age calculation"""
        age = self.patient.calculate_age()
        # Age should be around 34 (2024 - 1990)
        self.assertGreaterEqual(age, 33)
        self.assertLessEqual(age, 35)
    
    def test_update_contact_info(self):
        """Test updating contact information"""
        self.patient.update_contact_info("newemail@example.com", "11988888888")
        self.assertEqual(self.patient.email, "newemail@example.com")
        self.assertEqual(self.patient.phone, "11988888888")
    
    def test_patient_equality(self):
        """Test patient equality based on ID"""
        patient2 = Patient(
            id="patient-001",
            name="Different Name",
            date_of_birth=datetime(1990, 5, 15),
            gender="M",
            cpf="98765432109"
        )
        self.assertEqual(self.patient, patient2)


class TestProblemEntity(unittest.TestCase):
    """Tests for Problem entity (RCOP)"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.problem = Problem(
            id="problem-001",
            patient_id="patient-001",
            description="Hipertensão arterial sistêmica",
            icd10_code="I10",
            status="active"
        )
    
    def test_problem_creation(self):
        """Test problem creation"""
        self.assertEqual(self.problem.patient_id, "patient-001")
        self.assertEqual(self.problem.description, "Hipertensão arterial sistêmica")
        self.assertEqual(self.problem.status, "active")
    
    def test_resolve_problem(self):
        """Test resolving a problem"""
        self.problem.resolve_problem()
        self.assertEqual(self.problem.status, "resolved")
    
    def test_archive_problem(self):
        """Test archiving a problem"""
        self.problem.archive_problem()
        self.assertEqual(self.problem.status, "archived")
    
    def test_update_description(self):
        """Test updating problem description"""
        new_desc = "Hipertensão arterial sistêmica controlada"
        self.problem.update_description(new_desc)
        self.assertEqual(self.problem.description, new_desc)


class TestSOAPStructure(unittest.TestCase):
    """Tests for SOAP structure implementation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.subjective = Subjective(
            id="subj-001",
            clinical_record_id="record-001",
            patient_complaint="Dor de cabeça persistente",
            medical_history="Hipertensão",
            medications="Losartana 50mg",
            allergies="Penicilina"
        )
        
        self.objective = Objective(
            id="obj-001",
            clinical_record_id="record-001",
            vital_signs="PA: 150/95, FC: 72, FR: 16",
            physical_examination="Sem alterações"
        )
        
        self.assessment = Assessment(
            id="assess-001",
            clinical_record_id="record-001",
            diagnosis="Cefaleia tensional",
            clinical_impression="Relacionada à hipertensão não controlada",
            related_problems=["problem-001"]
        )
        
        self.plan = Plan(
            id="plan-001",
            clinical_record_id="record-001",
            treatment_plan="Repouso, analgésico e reavaliação",
            medications="Dipirona 500mg cada 6h"
        )
    
    def test_subjective_component(self):
        """Test subjective component"""
        self.assertEqual(self.subjective.patient_complaint, "Dor de cabeça persistente")
        self.assertEqual(self.subjective.medical_history, "Hipertensão")
        self.assertIsNotNone(self.subjective.created_at)
    
    def test_objective_component(self):
        """Test objective component"""
        self.assertIn("PA: 150/95", self.objective.vital_signs)
        self.assertEqual(self.objective.physical_examination, "Sem alterações")
    
    def test_assessment_component(self):
        """Test assessment component"""
        self.assertEqual(self.assessment.diagnosis, "Cefaleia tensional")
        self.assertIn("problem-001", self.assessment.related_problems)
    
    def test_plan_component(self):
        """Test plan component"""
        self.assertEqual(self.plan.treatment_plan, "Repouso, analgésico e reavaliação")
        self.assertIsNotNone(self.plan.medications)


class TestClinicalRecord(unittest.TestCase):
    """Tests for complete Clinical Record (RCOP/SOAP)"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.record = ClinicalRecord(
            id="record-001",
            patient_id="patient-001",
            professional_id="prof-001",
            problem_id="problem-001",
            encounter_date=datetime.now()
        )
    
    def test_clinical_record_creation(self):
        """Test clinical record creation"""
        self.assertEqual(self.record.patient_id, "patient-001")
        self.assertEqual(self.record.professional_id, "prof-001")
        self.assertFalse(self.record.is_complete())
    
    def test_add_soap_components(self):
        """Test adding SOAP components"""
        subjective = Subjective(
            id="subj-001",
            clinical_record_id="record-001",
            patient_complaint="Dolor"
        )
        
        objective = Objective(
            id="obj-001",
            clinical_record_id="record-001",
            vital_signs="Normal",
            physical_examination="OK"
        )
        
        assessment = Assessment(
            id="assess-001",
            clinical_record_id="record-001",
            diagnosis="Diagnóstico",
            clinical_impression="OK"
        )
        
        plan = Plan(
            id="plan-001",
            clinical_record_id="record-001",
            treatment_plan="Plan"
        )
        
        self.record.set_subjective(subjective)
        self.record.set_objective(objective)
        self.record.set_assessment(assessment)
        self.record.set_plan(plan)
        
        self.assertTrue(self.record.is_complete())


class TestAppointment(unittest.TestCase):
    """Tests for Appointment entity"""
    
    def setUp(self):
        """Set up test fixtures"""
        future_date = datetime(2025, 3, 15, 10, 30)
        self.appointment = Appointment(
            id="apt-001",
            patient_id="patient-001",
            professional_id="prof-001",
            appointment_date=future_date,
            reason="Consulta de rotina",
            status="scheduled"
        )
    
    def test_appointment_creation(self):
        """Test appointment creation"""
        self.assertEqual(self.appointment.patient_id, "patient-001")
        self.assertEqual(self.appointment.status, "scheduled")
    
    def test_mark_completed(self):
        """Test marking appointment as completed"""
        self.appointment.mark_completed("Paciente evolui bem")
        self.assertEqual(self.appointment.status, "completed")
        self.assertEqual(self.appointment.notes, "Paciente evolui bem")
    
    def test_cancel_appointment(self):
        """Test canceling an appointment"""
        self.appointment.cancel("Paciente solicitou cancelamento")
        self.assertEqual(self.appointment.status, "cancelled")
    
    def test_reschedule_appointment(self):
        """Test rescheduling an appointment"""
        new_date = datetime(2025, 3, 20, 14, 30)
        self.appointment.reschedule(new_date)
        self.assertEqual(self.appointment.appointment_date, new_date)


class TestBusinessRuleValidation(unittest.TestCase):
    """Tests for business rule validations"""
    
    def test_patient_invalid_gender(self):
        """Test patient with invalid gender"""
        # While not enforced in entity, it should be validated in use case
        patient = Patient(
            id="p-001",
            name="Test",
            date_of_birth=datetime(1990, 1, 1),
            gender="X",  # Invalid
            cpf="123456789"
        )
        # Entity accepts but use case should reject
        self.assertEqual(patient.gender, "X")
    
    def test_problem_status_transitions(self):
        """Test valid problem status transitions"""
        problem = Problem(
            id="prob-001",
            patient_id="p-001",
            description="Test",
            status="active"
        )
        self.assertEqual(problem.status, "active")
        
        problem.resolve_problem()
        self.assertEqual(problem.status, "resolved")
        
        # Once resolved, should not change again easily
        problem.resolve_problem()
        self.assertEqual(problem.status, "resolved")


if __name__ == "__main__":
    unittest.main()
