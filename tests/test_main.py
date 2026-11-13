
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app, get_db
from app.database import Base


# Create a separate in-memory test database
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


# Configure database for testing
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

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


# Test 1: Home API
def test_home(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "Running"


# Test 2: Health API
def test_health(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# Test 3: Create application
def test_create_application(client):
    response = client.post(
        "/applications",
        json={
            "company": "Google",
            "job_title": "Python Developer",
            "location": "Bangalore",
            "status": "Applied",
            "applied_date": "2026-11-13",
            "interview_date": None,
            "notes": "Testing application"
        }
    )

    assert response.status_code == 200
    assert response.json()["company"] == "Google"
    assert response.json()["id"] == 1


# Test 4: Get all applications
def test_get_applications(client):
    client.post(
        "/applications",
        json={
            "company": "Infosys",
            "job_title": "Software Engineer"
        }
    )

    response = client.get("/applications")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["company"] == "Infosys"


# Test 5: Update application
def test_update_application(client):
    create_response = client.post(
        "/applications",
        json={
            "company": "TCS",
            "job_title": "Python Developer"
        }
    )

    application_id = create_response.json()["id"]

    response = client.put(
        f"/applications/{application_id}",
        json={"status": "Interview"}
    )

    assert response.status_code == 200
    assert response.json()["status"] == "Interview"


# Test 6: Delete application
def test_delete_application(client):
    create_response = client.post(
        "/applications",
        json={
            "company": "Wipro",
            "job_title": "Backend Developer"
        }
    )

    application_id = create_response.json()["id"]

    response = client.delete(
        f"/applications/{application_id}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Application deleted successfully"

    get_response = client.get(
        f"/applications/{application_id}"
    )

    assert get_response.status_code == 404


# Test 7: Application not found
def test_application_not_found(client):
    response = client.get("/applications/999")

    assert response.status_code == 404


# Test 8: Search applications by company
def test_search_by_company(client):
    client.post("/applications", json={
        "company": "Google",
        "job_title": "Python Developer"
    })

    response = client.get("/applications?company=Google")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["company"] == "Google"


# Test 9: Filter applications by status
def test_filter_by_status(client):
    client.post("/applications", json={
        "company": "Infosys",
        "job_title": "Developer",
        "status": "Interview"
    })

    response = client.get("/applications?status=Interview")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["status"] == "Interview"


# Test 10: Filter applications by location
def test_filter_by_location(client):
    client.post("/applications", json={
        "company": "TCS",
        "job_title": "Data Engineer",
        "location": "Bangalore"
    })

    response = client.get("/applications?location=Bangalore")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["location"] == "Bangalore"


# Test 11: Combined filters
def test_combined_filters(client):
    client.post("/applications", json={
        "company": "Google",
        "job_title": "Python Developer",
        "location": "Bangalore",
        "status": "Interview"
    })

    response = client.get(
        "/applications?company=Google&status=Interview&location=Bangalore"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["company"] == "Google"


# Test 12: Pagination
def test_pagination(client):
    for company in ["Google", "Infosys", "TCS"]:
        response = client.post(
            "/applications",
            json={
                "company": company,
                "job_title": "Python Developer"
            }
        )
        assert response.status_code == 200

    response = client.get(
        "/applications?skip=0&limit=2"
    )

    assert response.status_code == 200
    assert len(response.json()) == 2


# Test 13: Sorting
def test_sorting(client):
    client.post("/applications", json={
        "company": "Google",
        "job_title": "Developer",
        "applied_date": "2026-11-01"
    })

    client.post("/applications", json={
        "company": "Infosys",
        "job_title": "Engineer",
        "applied_date": "2026-11-10"
    })

    response = client.get(
        "/applications?sort_order=desc"
    )

    assert response.status_code == 200

    applications = response.json()

    assert applications[0]["company"] == "Infosys"
    assert applications[1]["company"] == "Google"
