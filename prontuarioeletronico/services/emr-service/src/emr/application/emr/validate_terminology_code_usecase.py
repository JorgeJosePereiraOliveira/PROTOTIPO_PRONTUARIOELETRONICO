from dataclasses import dataclass
import re

from ...domain.__seedwork.use_case_interface import UseCase


@dataclass
class ValidateTerminologyCodeInputDTO:
    system: str
    code: str


@dataclass
class ValidateTerminologyCodeOutputDTO:
    system: str
    code: str
    status: str
    description: str
    valid: bool


class ValidateTerminologyCodeUseCase(
    UseCase[ValidateTerminologyCodeInputDTO, ValidateTerminologyCodeOutputDTO]
):
    _PATTERNS = {
        "cid": re.compile(r"^[A-TV-Z][0-9]{2}(\.[0-9A-Z]{1,4})?$"),
        "ciap": re.compile(r"^[A-Z][0-9]{2}$"),
        "sigtap": re.compile(r"^[0-9]{10}$"),
    }

    _CATALOG = {
        "cid": {
            "J45.9": "Asma nao especificada",
            "I10": "Hipertensao essencial primaria",
            "E11": "Diabetes mellitus tipo 2",
        },
        "ciap": {
            "R05": "Tosse",
            "K86": "Hipertensao sem complicacoes",
            "T90": "Diabetes nao insulinodependente",
        },
        "sigtap": {
            "0301010072": "Consulta medica em atencao primaria",
            "0301010080": "Consulta de retorno em atencao primaria",
            "0301060061": "Atendimento de urgencia em atencao basica",
        },
    }

    def execute(
        self, input_dto: ValidateTerminologyCodeInputDTO
    ) -> ValidateTerminologyCodeOutputDTO:
        system = input_dto.system.strip().lower()
        code = input_dto.code.strip().upper()

        if system not in self._PATTERNS:
            raise ValueError("system must be one of: cid, ciap, sigtap")
        if not code:
            raise ValueError("code is required")

        if self._PATTERNS[system].match(code) is None:
            raise ValueError(f"code format is invalid for system: {system}")

        description = self._CATALOG[system].get(code)
        if description is None:
            raise ValueError("code not found or inactive in terminology catalog")

        return ValidateTerminologyCodeOutputDTO(
            system=system,
            code=code,
            status="active",
            description=description,
            valid=True,
        )
