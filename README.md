# JobTrack – Job Application Management System

JobTrack is a REST API-based application that helps users manage and track their job applications in one place. It is built using Python, FastAPI, and SQLAlchemy with SQLite as the database.

## Features

- Create and manage job applications.
- View all job applications.
- Search applications by company name.
- Filter applications by status and location.
- Update application details.
- Delete job applications.
- Pagination and sorting.
- RESTful API documentation using Swagger UI.
- Automated testing using Pytest.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| SQLAlchemy | Database ORM |
| SQLite | Database |
| Pydantic | Data validation |
| Pytest | Automated testing |
| Uvicorn | ASGI server |

## Project Structure

```text
Job-Track/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   └── test_main.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/vaneeshpatel2004-vpc/Job-Track.git
cd Job-Track
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

## API Documentation

After starting the server, open:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
- Health Check: http://127.0.0.1:8000/health

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Welcome message |
| GET | `/health` | Health check |
| POST | `/applications` | Create an application |
| GET | `/applications` | Retrieve applications |
| GET | `/applications/{id}` | Retrieve one application |
| PUT | `/applications/{id}` | Update an application |
| DELETE | `/applications/{id}` | Delete an application |

### Example Job Application

```json
{
  "company": "Google",
  "job_title": "Python Developer",
  "location": "Bangalore",
  "status": "Applied",
  "notes": "Applied through company careers page"
}
```

## Running Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The project currently includes 13 automated tests covering API functionality, filtering, searching, pagination, sorting, and error handling.

## Future Enhancements

- User registration and login.
- JWT-based authentication.
- Personal job application dashboard.
- Interview scheduling and reminders.
- Application analytics and statistics.
- Cloud deployment.

## Author

**Vaneesh Patel**

GitHub: https://github.com/vaneeshpatel2004-vpc

---

*Built as a Python backend development portfolio project.*