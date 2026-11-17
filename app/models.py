from sqlalchemy import Column, Integer, String, Date, Text, Boolean, DateTime
from datetime import date, datetime, timezone
from app.database import Base



class JobApplication(Base):

    from sqlalchemy import ForeignKey
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String(100), nullable=False)

    job_title = Column(String(100), nullable=False)

    location = Column(String(100), nullable=True)

    status = Column(String(30), default="Applied")

    applied_date = Column(Date, default=date.today)

    interview_date = Column(Date, nullable=True)

    notes = Column(Text, nullable=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )
