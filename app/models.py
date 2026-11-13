
from sqlalchemy import Column, Integer, String, Date, Text
from datetime import date

from app.database import Base


class JobApplication(Base):

    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String(100), nullable=False)

    job_title = Column(String(100), nullable=False)

    location = Column(String(100), nullable=True)

    status = Column(String(30), default="Applied")

    applied_date = Column(Date, default=date.today)

    interview_date = Column(Date, nullable=True)

    notes = Column(Text, nullable=True)
