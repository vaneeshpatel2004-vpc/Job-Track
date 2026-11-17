
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db
from app.models import User
from app.security import hash_password


# Separate in-memory test database
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine
)


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestingSessionLocal() as db:
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password=hash_password("TestPassword123!")
        )
        db.add(user)

        second_user = User(
            username="seconduser",
            email="second@example.com",
            hashed_password=hash_password("SecondPassword123!")
        )
        db.add(second_user)
        db.commit()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def login_and_authorize(client, email, password):
    response = client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code == 200

    token = response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_user_login(client):
    headers = login_and_authorize(
        client,
        "test@example.com",
        "TestPassword123!"
    )
    assert headers["Authorization"].startswith("Bearer ")


def test_user_profile(client):
    headers = login_and_authorize(
        client,
        "test@example.com",
        "TestPassword123!"
    )

    response = client.get("/auth/me", headers=headers)

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_invalid_login(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_unauthorized_access(client):
    response = client.get("/applications")

    assert response.status_code == 403


def test_create_application(client):
    headers = login_and_authorize(
        client,
        "test@example.com",
        "TestPassword123!"
    )

    response = client.post(
        "/applications",
        headers=headers,
        json={
            "company": "Google",
            "job_title": "Python Developer",
            "location": "Bangalore",
            "status": "Applied"
        }
    )

    assert response.status_code == 201
    assert response.json()["company"] == "Google"


def test_get_applications(client):
    headers = login_and_authorize(
        client,
        "test@example.com",
        "TestPassword123!"
    )

    client.post(
        "/applications",
        headers=headers,
        json={
            "company": "Google",
            "job_title": "Python Developer"
        }
    )

    response = client.get("/applications", headers=headers)

    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_update_application(client):
    headers = login_and_authorize(
        client,
        "test@example.com",
        "TestPassword123!"
    )

    created = client.post(
        "/applications",
        headers=headers,
        json={
            "company": "Google",
            "job_title": "Python Developer"
        }
    )

    application_id = created.json()["id"]

    response = client.put(
        f"/applications/{application_id}",
        headers=headers,
        json={"status": "Interview"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Interview"


def test_delete_application(client):
    headers = login_and_authorize(
        client,
        "test@example.com",
        "TestPassword123!"
    )

    created = client.post(
        "/applications",
        headers=headers,
        json={
            "company": "Google",
            "job_title": "Python Developer"
        }
    )

    application_id = created.json()["id"]

    response = client.delete(
        f"/applications/{application_id}",
        headers=headers
    )

    assert response.status_code == 200


def test_user_cannot_access_another_users_application(client):
    first_user_headers = login_and_authorize(
        client,
        "test@example.com",
        "TestPassword123!"
    )

    second_user_headers = login_and_authorize(
        client,
        "second@example.com",
        "SecondPassword123!"
    )

    created = client.post(
        "/applications",
        headers=first_user_headers,
        json={
            "company": "Google",
            "job_title": "Python Developer"
        }
    )

    application_id = created.json()["id"]

    response = client.get(
        f"/applications/{application_id}",
        headers=second_user_headers
    )

    assert response.status_code == 404


def test_user_cannot_update_another_users_application(client):
    first_user_headers = login_and_authorize(
        client,
        "test@example.com",
        "TestPassword123!"
    )

    second_user_headers = login_and_authorize(
        client,
        "second@example.com",
        "SecondPassword123!"
    )

    created = client.post(
        "/applications",
        headers=first_user_headers,
        json={
            "company": "Google",
            "job_title": "Python Developer"
        }
    )

    application_id = created.json()["id"]

    response = client.put(
        f"/applications/{application_id}",
        headers=second_user_headers,
        json={"status": "Rejected"}
    )

    assert response.status_code == 404


def test_user_cannot_delete_another_users_application(client):
    first_user_headers = login_and_authorize(
        client,
        "test@example.com",
        "TestPassword123!"
    )

    second_user_headers = login_and_authorize(
        client,
        "second@example.com",
        "SecondPassword123!"
    )

    created = client.post(
        "/applications",
        headers=first_user_headers,
        json={
            "company": "Google",
            "job_title": "Python Developer"
        }
    )

    application_id = created.json()["id"]

    response = client.delete(
        f"/applications/{application_id}",
        headers=second_user_headers
    )

    assert response.status_code == 404
