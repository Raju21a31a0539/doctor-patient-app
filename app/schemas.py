from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class UserCreate(BaseModel):
    username: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class DoctorPaginationResponse(BaseModel):
    total: int
    current_page: int
    limit: int
    data: list[DoctorResponse]


class PatientPaginationResponse(BaseModel):
    total: int
    current_page: int
    limit: int
    data: list[PatientResponse]

class DoctorCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: str
    phone: str
    specialization: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits")

        return value


class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None and not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits")

        return value


class DoctorResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    specialization: str
    is_active: bool

    class Config:
        from_attributes = True


class PatientCreate(BaseModel):
    name: str = Field(..., min_length=2)
    age: int = Field(..., gt=0)
    phone: str
    doctor_id: int

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits")

        return value


class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    doctor_id: Optional[int] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None and not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits")

        return value


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    doctor_id: int

    class Config:
        from_attributes = True

class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    phone: str
    doctor_id: int

    class Config:
        from_attributes = True


class DoctorPaginationResponse(BaseModel):
    total: int
    current_page: int
    limit: int
    data: list[DoctorResponse]


class PatientPaginationResponse(BaseModel):
    total: int
    current_page: int
    limit: int
    data: list[PatientResponse]