from ..__seedwork.entity import Entity


class Patient(Entity):
    def __init__(
        self,
        id: str,
        name: str,
        cpf: str,
        date_of_birth: str,
        gender: str,
    ):
        super().__init__(id=id)
        self._name = name
        self._cpf = cpf
        self._date_of_birth = date_of_birth
        self._gender = gender

    @property
    def name(self) -> str:
        return self._name

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def date_of_birth(self) -> str:
        return self._date_of_birth

    @property
    def gender(self) -> str:
        return self._gender