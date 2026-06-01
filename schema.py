import uuid
from typing import Annotated, Optional, Text
from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints, Field
from models import Institute, JobMode, JobType, UserRole

# ---------------------------------------------------------------------------- #
#                                  AUTH SCHEMA                                 #
# ---------------------------------------------------------------------------- #


class RegisterRequest(BaseModel):
    model_config = ConfigDict(use_enum_values=True)
    username: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr
    password: Annotated[str, StringConstraints(max_length=100)]
    school: Annotated[Institute | None, Field(validate_default=True)] = None
    role: Annotated[UserRole, Field(validate_default=True)] = UserRole.STUDENT.value


class LoginRequest(BaseModel):
    username: Annotated[str | None, Field(validate_default=True)] = None
    email: Annotated[EmailStr | None, Field(validate_default=True)] = None
    password: str


# ---------------------------------------------------------------------------- #
#                                  USER SCHEMA                                 #
# ---------------------------------------------------------------------------- #


class UserBase(BaseModel):
    username: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr


class UserRequest(UserBase):
    model_config = ConfigDict(from_attributes=True)
    password: Annotated[str, StringConstraints(max_length=100)]
    school: Annotated[Institute, Field(validate_default=True)] = Institute.IITM.value
    role: UserRole


class UserUpdateRequest(BaseModel):
    username: Annotated[str | None, StringConstraints(max_length=50)] = None
    email: Annotated[EmailStr | None, StringConstraints(max_length=100)] = None
    password: Annotated[str | None, StringConstraints(max_length=100)] = None
    school: Annotated[Institute | None, Field(validate_default=True)] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: uuid.UUID
    school: Institute
    role: UserRole


# ---------------------------------------------------------------------------- #
#                                  JOBS SCHEMA                                 #
# ---------------------------------------------------------------------------- #


class JobBase(BaseModel):
    company_id: uuid.UUID
    title: Annotated[str, StringConstraints(max_length=100)]
    location: Annotated[str, StringConstraints(max_length=500)]
    description: Text


class JobRequest(JobBase):
    model_config = ConfigDict(from_attributes=True)
    mode: Annotated[JobMode, Field(validate_default=True)] = JobMode.ON_SITE.value
    job_type: Annotated[JobType, Field(validate_default=True)] = JobType.FULL_TIME.value


class JobResponse(JobBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    mode: JobMode
    job_type: JobType


# class UserResponse(BaseModel):
#     model_config = ConfigDict(from_attributes=True)
#     id: int
#     username: Annotated[str, StringConstraints(max_length=50)]
#     email: Annotated[EmailStr, StringConstraints(max_length=100)]
#     # password: Annotated[str, StringConstraints(max_length=100)]
#     school: Institute
