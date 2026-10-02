# ruff: noqa: E402, I001

import os

import pytest


os.environ["DATABASE_URL"] = "sqlite:///./test_vet_crm.db"
os.environ["SECRET_KEY"] = "test-secret-key"

from fastapi.testclient import TestClient

from app.db.session import Base, SessionLocal, engine
from app.main import app
from app.models.user import User, UserRole


@pytest.fixture(scope="session", autouse=True)
def database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(autouse=True)
def clean_database():
    db = SessionLocal()
    for table in reversed(Base.metadata.sorted_tables):
        db.execute(table.delete())
    db.commit()
    db.close()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def user(client):
    response = client.post(
        "/auth/register",
        json={"email": "user@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def admin():
    db = SessionLocal()
    admin = User(
        email="admin@example.com",
        hashed_password="",
        role=UserRole.admin,
    )
    from app.core.security import hash_password

    admin.hashed_password = hash_password("admin123")
    db.add(admin)
    db.commit()
    db.refresh(admin)
    result = {"id": admin.id, "email": admin.email}
    db.close()
    return result


@pytest.fixture
def auth_headers(client, user):
    response = client.post(
        "/auth/login",
        data={"username": user["email"], "password": "password123"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture
def admin_headers(client, admin):
    response = client.post(
        "/auth/login",
        data={"username": admin["email"], "password": "admin123"},
    )
    return {"Authorization": f"Bearer {response.json()['access_token']}"}
