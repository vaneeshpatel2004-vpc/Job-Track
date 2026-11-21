# JobTrack – Job Application Management System

JobTrack is a full-stack job application management system built using **Python, FastAPI, Streamlit, and SQLite**. It helps users organize their job applications, track application statuses, manage job information, and visualize their job-search progress through an interactive dashboard.

## Features

### User Authentication
- User registration and login.
- JWT-based authentication.
- Secure password hashing.
- User-specific application management.
- Protected user profile.

### Job Application Management
- Add new job applications.
- View, update, and delete applications.
- Search applications by company.
- Filter applications by status and location.
- Track application details and notes.

### Dashboard and Analytics
- Dashboard with application statistics.
- Overview of recent applications.
- Application status distribution using charts.
- Company-wise application analytics.
- Interactive Streamlit interface.

### Backend and Testing
- RESTful API using FastAPI.
- Database management using SQLAlchemy and SQLite.
- API documentation using Swagger UI.
- Automated testing using Pytest.
- User-level access control for application records.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| FastAPI | Backend REST API |
| Streamlit | Frontend and dashboard |
| SQLAlchemy | Database ORM |
| SQLite | Database |
| Pydantic | Data validation |
| PyJWT | JWT authentication |
| pwdlib | Password hashing |
| Pandas | Data processing |
| Plotly | Interactive charts |
| Requests | Frontend API communication |
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
│   ├── schemas.py
│   └── security.py
│
├── frontend/
│   ├── __init__.py
│   ├── main.py
│   ├── api.py
│   └── components.py
│
├── tests/
│   └── test_main.py
│
├── .gitignore
├── requirements.txt
└── README.md
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

### 5. Configure environment variables

Create a `.env` file in the project root directory.

Add the following:

```env
SECRET_KEY=your_generated_secret_key
```

Generate a secure secret key using Python:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the generated value into your `.env` file.

**Important:** Never upload your `.env` file or expose your secret key publicly.

## Running the Application

JobTrack uses two separate services: a FastAPI backend and a Streamlit frontend.

### 1. Start the FastAPI backend

Open the first terminal:

```powershell
uvicorn app.main:app --reload
```

Backend URL:

```text
http://127.0.0.1:8000
```

### 2. Start the Streamlit frontend

Open a second terminal, navigate to the project directory, and activate the virtual environment if necessary.

Run:

```powershell
streamlit run frontend/main.py
```

The Streamlit application will open in your browser.

Frontend URL:

```text
http://localhost:8501
```

**Note:** Keep both terminals running while using JobTrack locally.

## API Documentation

Once the FastAPI backend is running, access:

| Documentation | URL |
|---|---|
| Swagger UI | http://127.0.0.1:8000/docs |
| ReDoc | http://127.0.0.1:8000/redoc |
| Health Check | http://127.0.0.1:8000/health |

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

Authentication is required for protected application operations. Refer to Swagger UI for the complete API schemas and authentication requirements.

## Example Job Application

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

```powershell
python -m pytest -v
```

The project currently includes **13 automated tests**, covering:

- Home and health endpoints.
- User login and profile.
- Invalid login and unauthorized access.
- Creating, retrieving, updating, and deleting applications.
- Preventing users from accessing or modifying another user's applications.

## Future Enhancements

- Interview scheduling and reminders.
- Email notifications for application updates.
- Resume management and tracking.
- Advanced job-search analytics.
- Cloud deployment.

## Author

**Vaneesh Patel**

GitHub: [vaneeshpatel2004-vpc](https://github.com/vaneeshpatel2004-vpc)

Project Repository: [JobTrack](https://github.com/vaneeshpatel2004-vpc/Job-Track)

---

*Built as a Python full-stack development portfolio project.*
