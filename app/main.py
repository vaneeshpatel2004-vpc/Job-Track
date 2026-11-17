
from typing import Optional

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app import models, schemas
from app.auth import router as auth_router, get_current_user


# Create database tables
Base.metadata.create_all(bind=engine)


# Initialize FastAPI
app = FastAPI(
    title="JobTrack API",
    description="Job Application Management System with JWT Authentication",
    version="2.0.0"
)


# Register authentication routes
app.include_router(auth_router)


# --------------------------------------------------
# HOME AND HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to JobTrack API"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# CREATE JOB APPLICATION
# --------------------------------------------------

@app.post(
    "/applications",
    response_model=schemas.JobApplicationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_application(
    application: schemas.JobApplicationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_application = models.JobApplication(
        **application.model_dump(),
        user_id=current_user.id
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application


# --------------------------------------------------
# GET ALL APPLICATIONS BELONGING TO CURRENT USER
# --------------------------------------------------

@app.get("/applications")
def get_applications(
    company: Optional[str] = None,
    application_status: Optional[str] = Query(
        default=None,
        alias="status"
    ),
    location: Optional[str] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    sort_order: str = Query(default="desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    query = db.query(models.JobApplication).filter(
        models.JobApplication.user_id == current_user.id
    )

    if company:
        query = query.filter(
            models.JobApplication.company.ilike(f"%{company}%")
        )

    if application_status:
        query = query.filter(
            models.JobApplication.status.ilike(
                f"%{application_status}%"
            )
        )

    if location:
        query = query.filter(
            models.JobApplication.location.ilike(f"%{location}%")
        )

    if sort_order == "asc":
        query = query.order_by(
            models.JobApplication.applied_date.asc(),
            models.JobApplication.id.asc()
        )
    else:
        query = query.order_by(
            models.JobApplication.applied_date.desc(),
            models.JobApplication.id.desc()
        )

    total = query.count()

    applications = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "applications": applications
    }


# --------------------------------------------------
# GET SINGLE JOB APPLICATION
# --------------------------------------------------

@app.get(
    "/applications/{application_id}",
    response_model=schemas.JobApplicationResponse
)
def get_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id,
        models.JobApplication.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return application


# --------------------------------------------------
# UPDATE JOB APPLICATION
# --------------------------------------------------

@app.put(
    "/applications/{application_id}",
    response_model=schemas.JobApplicationResponse
)
def update_application(
    application_id: int,
    application_data: schemas.JobApplicationUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id,
        models.JobApplication.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    update_data = application_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(application, key, value)

    db.commit()
    db.refresh(application)

    return application


# --------------------------------------------------
# DELETE JOB APPLICATION
# --------------------------------------------------

@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id,
        models.JobApplication.user_id == current_user.id
    ).first()

    if not application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Job application deleted successfully"
    }
