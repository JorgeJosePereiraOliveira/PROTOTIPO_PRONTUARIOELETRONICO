"""
FastAPI Main Application
Entry point for the Prontuário Eletrônico API
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .config import create_app
from .routers import patient_routers, clinical_record_routers, professional_routers

# Create the FastAPI application
app = create_app()

# Include routers
app.include_router(patient_routers.router)
app.include_router(clinical_record_routers.router)
app.include_router(professional_routers.router)


@app.get("/")
def read_root():
    """
    Root endpoint - Health check
    """
    return {
        "message": "Prontuário Eletrônico API - Clean Architecture",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/api/v1")
def api_info():
    """API information endpoint"""
    return {
        "title": "Prontuário Eletrônico API",
        "description": "Electronic Patient Record System following Clean Architecture principles",
        "version": "1.0.0",
        "architecture": "Clean Architecture (RCOP/SOAP)",
        "endpoints": {
            "patients": "/api/v1/patients",
            "clinical_records": "/api/v1/clinical-records"
        }
    }


@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    """Handle ValueError exceptions"""
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
