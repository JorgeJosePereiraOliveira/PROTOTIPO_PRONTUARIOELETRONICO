import unittest
from datetime import datetime
from prontuarioeletronico.src.application.appointment.schedule_appointment_usecase import ScheduleAppointmentUseCase, ScheduleAppointmentDTO
from prontuarioeletronico.src.domain.appointment.appointment_entity import Appointment

class FakeAppointmentRepository:
    def __init__(self):
        self.data = {}
    def save(self, appointment):
        self.data[appointment.id] = appointment
    def add(self, appointment):
        self.save(appointment)
    def update(self, appointment):
        self.data[appointment.id] = appointment
    def find_by_id(self, appointment_id):
        return self.data.get(appointment_id)
    def delete(self, appointment_id):
        self.data.pop(appointment_id, None)

class TestScheduleAppointmentUseCase(unittest.TestCase):
    def setUp(self):
        self.repo = FakeAppointmentRepository()
        self.dto = ScheduleAppointmentDTO(
            patient_id='p1',
            professional_id='pr1',
            appointment_date=datetime(2026, 2, 23, 10, 0),
            reason='Consulta de rotina',
            notes='Nenhuma'
        )
    def test_schedule_appointment(self):
        usecase = ScheduleAppointmentUseCase(self.repo)
        # Mock _generate_id and _validate_input
        usecase._generate_id = lambda: 'a1'
        usecase._validate_input = lambda x: None
        output = usecase.execute(self.dto)
        self.assertEqual(output.appointment_id, 'a1')
        self.assertEqual(self.repo.data['a1'].reason, 'Consulta de rotina')

if __name__ == '__main__':
    unittest.main()
