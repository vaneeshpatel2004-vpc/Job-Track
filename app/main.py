
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal
from app import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JobTrack API",
    description="Job Application Management System",
    version="1.0.0"
)


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Welcome to JobTrack!",
        "status": "Running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# CREATE: Add a job application
@app.post("/applications", response_model=schemas.JobApplicationResponse)
def create_application(
    application: schemas.JobApplicationCreate,
    db: Session = Depends(get_db)
):
    new_application = models.JobApplication(**application.model_dump())

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application



from typing import Optional
from fastapi import Query

@app.get(
    "/applications",
    response_model=list[schemas.JobApplicationResponse]
)
def get_applications(
    company: Optional[str] = None,
    status: Optional[str] = None,
    location: Optional[str] = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    sort_order: str = Query(
        default="desc",
        pattern="^(asc|desc)$"
    ),
    db: Session = Depends(get_db)
):
    query = db.query(models.JobApplication)

    # Search by company
    if company:
        query = query.filter(
            models.JobApplication.company.ilike(
                f"%{company}%"
            )
        )

    # Filter by status
    if status:
        query = query.filter(
            models.JobApplication.status.ilike(status)
        )

    # Filter by location
    if location:
        query = query.filter(
            models.JobApplication.location.ilike(
                f"%{location}%"
            )
        )

    # Sort by applied date and ID
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

    # Apply pagination
    return query.offset(skip).limit(limit).all()




# READ: Get one job application
@app.get("/applications/{application_id}", response_model=schemas.JobApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id
    ).first()

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    return application

# UPDATE: Modify a job application
@app.put("/applications/{application_id}",
         response_model=schemas.JobApplicationResponse)
def update_application(
    application_id: int,
    updated_data: schemas.JobApplicationUpdate,
    db: Session = Depends(get_db)
):
    application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    update_fields = updated_data.model_dump(exclude_unset=True)

    for key, value in update_fields.items():
        setattr(application, key, value)

    db.commit()
    db.refresh(application)

    return application


# DELETE: Remove a job application
@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = db.query(models.JobApplication).filter(
        models.JobApplication.id == application_id
    ).first()

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Application deleted successfully"
    }
