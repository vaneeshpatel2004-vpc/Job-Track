
from pydantic import BaseModel
from datetime import date
from typing import Optional


class JobApplicationCreate(BaseModel):
    company: str
    job_title: str
    location: Optional[str] = None
    status: str = "Applied"
    applied_date: date = date.today()
    interview_date: Optional[date] = None
    notes: Optional[str] = None


class JobApplicationResponse(BaseModel):
    id: int
    company: str
    job_title: str
    location: Optional[str]
    status: str
    applied_date: date
    interview_date: Optional[date]
    notes: Optional[str]

    class Config:
        from_attributes = True


class JobApplicationUpdate(BaseModel):
    company: Optional[str] = None
    job_title: Optional[str] = None
    location: Optional[str] = None
    status: Optional[str] = None
    applied_date: Optional[date] = None
    interview_date: Optional[date] = None
    notes: Optional[str] = None


from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
