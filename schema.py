import uuid
from decimal import Decimal
from typing import Annotated, Optional, Text, Literal
from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints, Field
from models import Institute, JobMode, JobType, UserRole, CompanyStatus

# ---------------------------------------------------------------------------- #
#                                  AUTH SCHEMA                                 #
# ---------------------------------------------------------------------------- #

class RegisterUserBase(BaseModel):
    username: Annotated[str, StringConstraints(max_length=50)]
    email: EmailStr

class RegisterUserRequest(RegisterUserBase):
    password: Annotated[str, StringConstraints(max_length=100)]

class RegisterStudentRequest(RegisterUserRequest):
    model_config = ConfigDict(use_enum_values=True)
    first_name: Annotated[str, StringConstraints(max_length=100)]
    last_name: Annotated[str, StringConstraints(max_length=100)]
    school: Annotated[str, StringConstraints(max_length=500)]
    cgpa: Annotated[Decimal, Field(ge=0, le=10, decimal_places=1)]
    role: Annotated[UserRole, Field(validate_default=True)] = UserRole.STUDENT

class RegisterCompanyRequest(RegisterUserRequest):
    # user_id: uuid.UUID
    name: Annotated[str, StringConstraints(max_length=100)]
    website: Annotated[str, StringConstraints(max_length=200)]
    about: str
    location: Annotated[str, StringConstraints(max_length=500)]
    role: Literal[UserRole.COMPANY.value]

class ValidateRegisteredStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    user_id: uuid.UUID
    first_name: Annotated[str, StringConstraints(max_length=100)]
    last_name: Annotated[str, StringConstraints(max_length=100)]
    school: Annotated[str, StringConstraints(max_length=500)]
    cgpa: Annotated[Decimal, Field(ge=0, le=10, decimal_places=1)]

class ValidateRegisteredCompany(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    user_id: uuid.UUID
    name: Annotated[str, StringConstraints(max_length=100)]
    website: Annotated[str, StringConstraints(max_length=200)]
    about: str
    location: Annotated[str, StringConstraints(max_length=500)]

class RegisterUserResponse(RegisterUserBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    student_profile: ValidateRegisteredStudent | None
    company_profile: ValidateRegisteredCompany | None
    role: UserRole

class StudentResponse(RegisterUserBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    student_profile: ValidateRegisteredStudent | None
    role: Literal[UserRole.STUDENT]

class CompanyResponse(RegisterUserBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    company_profile: ValidateRegisteredCompany | None
    role: Literal[UserRole.COMPANY]

class RegisterCompanyResponse(RegisterCompanyRequest):
    model_config = ConfigDict(from_attributes=True ,use_enum_values=True)
    status: CompanyStatus = CompanyStatus.PENDING.value

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
    role: UserRole

class UserUpdateRequest(BaseModel):
    username: Annotated[str | None, StringConstraints(max_length=50)] = None
    email: Annotated[EmailStr | None, StringConstraints(max_length=100)] = None
    password: Annotated[str | None, StringConstraints(max_length=100)] = None

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: uuid.UUID
    username: str
    email: EmailStr
    role: UserRole
    student_profile: Optional[ValidateRegisteredStudent] = None
    company_profile: Optional[ValidateRegisteredCompany] = None

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
