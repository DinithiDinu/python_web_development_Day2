import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.database import Base, get_db
from app.main import app
from app.models import models  # noqa: F401

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)   
    app.dependency_overrides.clear()


@pytest.fixture()
def department(client):
    response = client.post("/departments", json={"department_name": "Engineering"})
    return response.json()


@pytest.fixture()
def employee_payload(department):
    return {
        "name": "Dinithi",
        "email": "dinithi@mail.com",
        "department_id": department["department_id"],
        "salary": 60000,
        "status": "Active",
    }