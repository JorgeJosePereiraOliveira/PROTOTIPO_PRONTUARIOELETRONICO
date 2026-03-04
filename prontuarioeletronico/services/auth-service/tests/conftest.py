import os


def pytest_sessionstart(session):
    os.environ.setdefault("APP_ENV", "test")
    os.environ.setdefault("AUTH_JWT_SECRET", "test-secret-ms01")
    os.environ.setdefault("AUTH_DATABASE_URL", "sqlite:///./test_auth.db")
