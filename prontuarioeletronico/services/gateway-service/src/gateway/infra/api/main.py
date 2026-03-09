import os

from fastapi import FastAPI, Header, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict

from ..proxy.http_service_proxy import HttpServiceProxy


app = FastAPI(
    title="Gateway Service",
    version="1.0.0",
    description="API Gateway para roteamento de Auth e Patient Services",
)


class LoginRequest(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "admin",
                "password": "admin123",
            }
        }
    )


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class PatientPayload(BaseModel):
    name: str
    cpf: str
    date_of_birth: str
    gender: str


class ProblemPayload(BaseModel):
    patient_id: str
    description: str
    status: str = "active"


class SOAPPayload(BaseModel):
    problem_id: str
    patient_id: str
    professional_id: str
    subjective: str
    objective: str
    assessment: str
    plan: str


APP_ENV = os.getenv("APP_ENV", "development")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
PATIENT_SERVICE_URL = os.getenv("PATIENT_SERVICE_URL")
EMR_SERVICE_URL = os.getenv("EMR_SERVICE_URL")

if APP_ENV in {"production", "staging"}:
    if AUTH_SERVICE_URL is None:
        raise RuntimeError("AUTH_SERVICE_URL is required for production/staging")
    if PATIENT_SERVICE_URL is None:
        raise RuntimeError("PATIENT_SERVICE_URL is required for production/staging")
    if EMR_SERVICE_URL is None:
        raise RuntimeError("EMR_SERVICE_URL is required for production/staging")

if AUTH_SERVICE_URL is None:
    AUTH_SERVICE_URL = "http://localhost:8001"
if PATIENT_SERVICE_URL is None:
    PATIENT_SERVICE_URL = "http://localhost:8002"
if EMR_SERVICE_URL is None:
    EMR_SERVICE_URL = "http://localhost:8003"

_auth_proxy = HttpServiceProxy(base_url=AUTH_SERVICE_URL)
_patient_proxy = HttpServiceProxy(base_url=PATIENT_SERVICE_URL)
_emr_proxy = HttpServiceProxy(base_url=EMR_SERVICE_URL)


def _forward_response(status_code: int, body: object) -> JSONResponse:
    return JSONResponse(status_code=status_code, content=body)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "gateway"}


@app.get("/api/v1/info")
def service_info():
    return {
        "service": "gateway",
        "architecture": "clean-architecture",
        "layers": ["domain", "application", "infra"],
        "routes": ["auth", "patients", "emr"],
    }


@app.post("/api/v1/auth/login")
def auth_login(payload: LoginRequest):
    status_code, body = _auth_proxy.request(
        method="POST",
        path="/api/v1/auth/login",
        json_body=payload.model_dump(),
    )
    return _forward_response(status_code, body)


@app.post("/api/v1/auth/refresh")
def auth_refresh(payload: RefreshRequest):
    status_code, body = _auth_proxy.request(
        method="POST",
        path="/api/v1/auth/refresh",
        json_body=payload.model_dump(),
    )
    return _forward_response(status_code, body)


@app.post("/api/v1/auth/logout")
def auth_logout(payload: LogoutRequest, authorization: str | None = Header(default=None)):
    status_code, body = _auth_proxy.request(
        method="POST",
        path="/api/v1/auth/logout",
        json_body=payload.model_dump(),
        authorization=authorization,
    )
    return _forward_response(status_code, body)


@app.get("/api/v1/auth/verify")
def auth_verify(authorization: str | None = Header(default=None)):
    status_code, body = _auth_proxy.request(
        method="GET",
        path="/api/v1/auth/verify",
        authorization=authorization,
    )
    return _forward_response(status_code, body)


@app.get("/api/v1/auth/authorize")
def auth_authorize(
    required_role: str = Query(...),
    authorization: str | None = Header(default=None),
):
    status_code, body = _auth_proxy.request(
        method="GET",
        path="/api/v1/auth/authorize",
        authorization=authorization,
        params={"required_role": required_role},
    )
    return _forward_response(status_code, body)


@app.post("/api/v1/patients")
def create_patient(payload: PatientPayload, authorization: str | None = Header(default=None)):
    status_code, body = _patient_proxy.request(
        method="POST",
        path="/api/v1/patients",
        json_body=payload.model_dump(),
        authorization=authorization,
    )
    return _forward_response(status_code, body)


@app.get("/api/v1/patients")
def list_patients(authorization: str | None = Header(default=None)):
    status_code, body = _patient_proxy.request(
        method="GET",
        path="/api/v1/patients",
        authorization=authorization,
    )
    return _forward_response(status_code, body)


@app.get("/api/v1/patients/{patient_id}")
def get_patient(patient_id: str, authorization: str | None = Header(default=None)):
    status_code, body = _patient_proxy.request(
        method="GET",
        path=f"/api/v1/patients/{patient_id}",
        authorization=authorization,
    )
    return _forward_response(status_code, body)


@app.put("/api/v1/patients/{patient_id}")
def update_patient(
    patient_id: str,
    payload: PatientPayload,
    authorization: str | None = Header(default=None),
):
    status_code, body = _patient_proxy.request(
        method="PUT",
        path=f"/api/v1/patients/{patient_id}",
        json_body=payload.model_dump(),
        authorization=authorization,
    )
    return _forward_response(status_code, body)


@app.delete("/api/v1/patients/{patient_id}")
def delete_patient(patient_id: str, authorization: str | None = Header(default=None)):
    status_code, body = _patient_proxy.request(
        method="DELETE",
        path=f"/api/v1/patients/{patient_id}",
        authorization=authorization,
    )
    return _forward_response(status_code, body)


@app.post("/api/v1/emr/problems")
def create_problem(payload: ProblemPayload, authorization: str | None = Header(default=None)):
    status_code, body = _emr_proxy.request(
        method="POST",
        path="/api/v1/emr/problems",
        json_body=payload.model_dump(),
        authorization=authorization,
    )
    return _forward_response(status_code, body)


@app.get("/api/v1/emr/problems/{problem_id}")
def get_problem(problem_id: str, authorization: str | None = Header(default=None)):
    status_code, body = _emr_proxy.request(
        method="GET",
        path=f"/api/v1/emr/problems/{problem_id}",
        authorization=authorization,
    )
    return _forward_response(status_code, body)


@app.post("/api/v1/emr/soap")
def create_soap(payload: SOAPPayload, authorization: str | None = Header(default=None)):
    status_code, body = _emr_proxy.request(
        method="POST",
        path="/api/v1/emr/soap",
        json_body=payload.model_dump(),
        authorization=authorization,
    )
    return _forward_response(status_code, body)


@app.get("/api/v1/emr/soap/{soap_id}")
def get_soap(soap_id: str, authorization: str | None = Header(default=None)):
    status_code, body = _emr_proxy.request(
        method="GET",
        path=f"/api/v1/emr/soap/{soap_id}",
        authorization=authorization,
    )
    return _forward_response(status_code, body)
