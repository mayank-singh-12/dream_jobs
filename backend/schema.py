from models import JobStatus
from decimal import Decimal
from typing import Annotated, Optional, Text, Literal
from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints, Field
from models import JobMode, JobType, UserRole, CompanyStatus, StudentStatus, ApplicationStatus
from datetime import datetime

# ---------------------------------------------------------------------------- #
#                                  AUTH SCHEMA                                 #
# ---------------------------------------------------------------------------- #


class RegisterUserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
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
    phone_number: Annotated[str, StringConstraints(max_length=20)]
    role: Literal[UserRole.STUDENT] = UserRole.STUDENT

class RegisterCompanyRequest(RegisterUserRequest):
    model_config = ConfigDict(use_enum_values=True)
    name: Annotated[str, StringConstraints(max_length=100)]
    website: Annotated[str, StringConstraints(max_length=200)]
    about: str
    location: Annotated[str, StringConstraints(max_length=500)]
    role: Literal[UserRole.COMPANY] = UserRole.COMPANY

class ValidateRegisteredStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True,use_enum_values=True)
    id: int
    first_name: Annotated[str, StringConstraints(max_length=100)]
    last_name: Annotated[str, StringConstraints(max_length=100)]
    school: Annotated[str, StringConstraints(max_length=500)]
    cgpa: Annotated[Decimal, Field(ge=0, le=10, decimal_places=1)]
    status: StudentStatus = StudentStatus.ACTIVE
    resume_path: Optional[str] = None
    phone_number: Annotated[Optional[str], StringConstraints(max_length=20)] = None

class ValidateRegisteredCompany(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    name: Annotated[str, StringConstraints(max_length=100)]
    website: Annotated[str, StringConstraints(max_length=200)]
    about: str
    location: Annotated[str, StringConstraints(max_length=500)]
    status: CompanyStatus

class StudentResponse(RegisterUserBase):
    id: int
    student_profile: ValidateRegisteredStudent | None
    role: Literal[UserRole.STUDENT]
    
class CompanyResponse(RegisterUserBase):
    id: int
    company_profile: ValidateRegisteredCompany | None
    role: Literal[UserRole.COMPANY]

class CompanyResponseForStudent(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    company_profile: ValidateRegisteredCompany | None

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
    id: int
    username: str
    email: EmailStr
    role: UserRole
    student_profile: Optional[ValidateRegisteredStudent] = None
    company_profile: Optional[ValidateRegisteredCompany] = None

# ---------------------------------------------------------------------------- #
#                                  JOBS SCHEMA                                 #
# ---------------------------------------------------------------------------- #

class JobBase(BaseModel):
    title: Annotated[str, StringConstraints(max_length=100)]
    location: Annotated[str, StringConstraints(max_length=500)]
    description: Text

class JobRequest(JobBase):
    model_config = ConfigDict(from_attributes=True)
    mode: Annotated[JobMode, Field(validate_default=True)] = JobMode.ON_SITE.value
    job_type: Annotated[JobType, Field(validate_default=True)] = JobType.FULL_TIME.value
    required_cgpa: Optional[Decimal] = None
    deadline: Optional[datetime] = None

class JobResponse(JobBase):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    mode: JobMode
    job_type: JobType
    job_status: JobStatus
    required_cgpa: Optional[Decimal] = None
    deadline: Optional[datetime] = None
    company: Optional[ValidateRegisteredCompany] = None

class JobResponseForCompany(JobResponse):
    application_count: int = 0

# ---------------------------- APPLICATION SCHEMA ---------------------------- #

class ApplicationRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    job_id: int

class ApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    student_id: int
    job_id: Optional[int]
    status: ApplicationStatus
    applied_at: datetime


class StudentApplicationResponse(ApplicationResponse):
    job: Optional[JobResponse] = None


class AdminJobCompanyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    name: str

class AdminJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    title: str
    location: str
    mode: str
    job_type: str
    required_cgpa: Optional[float] = None
    company: Optional[AdminJobCompanyResponse] = None

class AdminStudentProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    first_name: str
    last_name: str
    school: str
    cgpa: float
    phone_number: Optional[str] = None

class AdminApplicationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int
    student_id: int
    job_id: Optional[int]
    status: ApplicationStatus
    applied_at: datetime
    student: Optional[AdminStudentProfileResponse] = None
    job: Optional[AdminJobResponse] = None


# ----------------------------- UPDATE SCHEMAS ------------------------------- #

class StudentUpdateRequest(BaseModel):
    first_name: Annotated[Optional[str], StringConstraints(max_length=100)] = None
    last_name: Annotated[Optional[str], StringConstraints(max_length=100)] = None
    school: Annotated[Optional[str], StringConstraints(max_length=500)] = None
    cgpa: Annotated[Optional[Decimal], Field(default=None, ge=0, le=10, decimal_places=1)] = None
    phone_number: Annotated[Optional[str], StringConstraints(max_length=20)] = None

class CompanyUpdateRequest(BaseModel):
    name: Annotated[Optional[str], StringConstraints(max_length=100)] = None
    website: Annotated[Optional[str], StringConstraints(max_length=200)] = None
    about: Optional[str] = None
    location: Annotated[Optional[str], StringConstraints(max_length=500)] = None