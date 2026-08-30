from sqlalchemy.orm import joinedload
from models import StudentStatus
from schema import JobResponse
from flask_jwt_extended import jwt_required, current_user, verify_jwt_in_request
import json
from flask import request, jsonify, current_app, Response
from sqlalchemy import select, func, or_
from database import SessionLocal
from models import (
    User,
    Job,
    UserRole,
    StudentProfile,
    JobStatus,
    CompanyProfile,
    CompanyStatus,
    Application
)
from schema import (
    StudentResponse,
    CompanyResponse,
    AdminApplicationResponse
)
from pydantic import ValidationError
from flask import Blueprint

admin = Blueprint("admin", __name__, url_prefix="/api/admin")


@admin.before_request
@jwt_required()
def only_admins():
    if request.method == "OPTIONS":
        return

    verify_jwt_in_request()

    if current_user.role != UserRole.ADMIN:
        return (
            jsonify({"message": "You are not allowed to access this route."}),
            403,
        )


# --------------------------------- COMPANIES -------------------------------- #

# get all comapnies
@admin.get("/company")
def get_all_companies():
    try:
        query = request.args.get("q", "").strip()
        current_app.logger.debug(query)

        with SessionLocal() as db:
            stmt = (
                select(User).join(CompanyProfile).where(User.role == UserRole.COMPANY)
            )
            if query:
                stmt = stmt.where(
                    or_(
                        CompanyProfile.name.like(f"{query}%"),
                        CompanyProfile.location.like(f"{query}%"),
                        User.username.like(f"{query}%"),
                        User.email.like(f"{query}%"),
                    )
                )
            companies = db.scalars(stmt).all()
            current_app.logger.debug(f"\n-----companies-----{companies}\n")
            results = [
                CompanyResponse.model_validate(company).model_dump()
                for company in companies
            ]
            current_app.logger.debug(f"\n-----results-----\n{results}\n")
        return jsonify({"data": results})

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# approve a company
@admin.post("/company/<int:company_id>/approved")
def approve_company(company_id):
    try:
        with SessionLocal() as db:
            company = db.get(CompanyProfile, company_id)

            if company is None:
                return jsonify({"message": "Company no longer exists."}), 404

            if company.status == CompanyStatus.APPROVED:
                return jsonify({"message": "Company is already approved."}), 400

            current_app.logger.debug(f"COMPANY ----------> \n {company}")

            company.status = CompanyStatus.APPROVED
            current_app.logger.debug(f"NEW STATUS ---> {company.status}")
            db.commit()

        return jsonify({"message": "Company approved!"}), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# reject a company
@admin.post("/company/<int:company_id>/rejected")
def reject_company(company_id):
    try:
        with SessionLocal() as db:
            company = db.get(CompanyProfile, company_id)
            if company is None:
                return jsonify({"message": "Company no longer exists."}), 404
            if company.status == CompanyStatus.REJECTED:
                return jsonify({"message": "Company is already rejected."}), 400
            company.status = CompanyStatus.REJECTED
            db.commit()
        return jsonify({"message": "Company rejected!"}), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# make company pending
@admin.post("/company/<int:company_id>/pending")
def pending_company(company_id):
    try:
        with SessionLocal() as db:
            company = db.get(CompanyProfile, company_id)
            if company is None:
                return jsonify({"message": "Company no longer exists."}), 404
            if company.status == CompanyStatus.PENDING:
                return jsonify({"message": "Company is already pending."}), 400
            company.status = CompanyStatus.PENDING
            db.commit()
            
        return jsonify({"message": "Company pending!"}), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# get company detail
@admin.get("/company/<int:company_id>")
def get_company_detail(company_id):
    try:
        print(company_id)
        with SessionLocal() as db:
            stmt = select(User).join(CompanyProfile).where(CompanyProfile.id ==company_id)
            company = db.scalars(stmt).one_or_none()
            if company is None:
                return jsonify({"message": "Company no longer exists."}), 404
            result = CompanyResponse.model_validate(company).model_dump()
        return jsonify({"data": result}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# ------------------------------ PLACEMENT DRIVE ----------------------------- #

# get all placement drives
@admin.get("/jobs")
def get_all_jobs():
    try:
        with SessionLocal() as db:
            stmt = select(Job)
            jobs = db.scalars(stmt).all()
            jobs_data = [JobResponse.model_validate(job).model_dump() for job in jobs]
        return jsonify(jobs_data),200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# approve a placement drive
@admin.post("/job/<int:job_id>/approve")
def approve_placement_drive(job_id):
    try:
        with SessionLocal() as db:
            job = db.get(Job, job_id)
            if job is None:
                return jsonify({"message": "Job no longer exists."}), 404
            if job.job_status == JobStatus.APPROVED:
                return jsonify({"message": "Job is already approved."}), 400
            job.job_status = JobStatus.APPROVED
            current_app.logger.debug(
                f"UPDATED JOB STATUS --------------> \n {job.job_status}"
            )
            db.commit()
        return jsonify({"message": "Job approved!"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# reject a placement drive
@admin.post("/job/<int:job_id>/reject")
def reject_placement_drive(job_id):
    try:
        with SessionLocal() as db:
            job = db.get(Job, job_id)
            if job is None:
                return jsonify({"message": "Job no longer exists."}), 404
            if job.job_status == JobStatus.REJECTED:
                return jsonify({"message": "Job is already rejected."}), 400
            job.job_status = JobStatus.REJECTED
            current_app.logger.debug(
                f"UPDATED JOB STATUS --------------> \n {job.job_status}"
            )
            db.commit()
        return jsonify({"message": "Job rejected!"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# pending a placement drive
@admin.post("/job/<int:job_id>/pending")
def pending_placement_drive(job_id):
    try:
        with SessionLocal() as db:
            job = db.get(Job, job_id)
            if job is None:
                return jsonify({"message": "Job no longer exists."}), 404
            if job.job_status == JobStatus.PENDING:
                return jsonify({"message": "Job is already pending."}), 400
            job.job_status = JobStatus.PENDING
            current_app.logger.debug(
                f"UPDATED JOB STATUS --------------> \n {job.job_status}"
            )
            db.commit()
        return jsonify({"message": "Job pending!"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# --------------------------------- STUDENTS --------------------------------- #

# get all students
@admin.get("/students")
def get_all_students():
    try:
        query = request.args.get("q", "").strip()
        with SessionLocal() as db:
            stmt = (
                select(User).join(StudentProfile).where(User.role == UserRole.STUDENT)
            )
            if query:
                stmt = stmt.where(
                    or_(
                        User.email.like(f"{query}%"),
                        User.username.like(f"{query}%"),
                        StudentProfile.first_name.like(f"{query}%"),
                        StudentProfile.last_name.like(f"{query}%"),
                        User.email.like(f"{query}%"),
                    )
                )
            students = db.scalars(stmt).all()
            current_app.logger.debug(f"\n-----students-----{students}\n")
            results = [
                StudentResponse.model_validate(student).model_dump(mode="json")
                for student in students
            ]
            current_app.logger.debug(f"\n-----results-----\n{results}\n")
            response_data = json.dumps({"data": results})
        return Response(response_data, mimetype="application/json"), 200

    except ValidationError as ve:
        current_app.logger.error(ve)
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500


# blacklist student
@admin.post("/student/<int:student_id>/blacklist")
def pending_student(student_id):
    try:
        with SessionLocal() as db:
            student = db.get(StudentProfile, student_id)
            if student is None:
                return jsonify({"message": "Student no longer exists."}), 404
            if student.status == StudentStatus.BLACKLISTED:
                return jsonify({"message": "Student is already blacklisted."}), 400
            student.status = StudentStatus.BLACKLISTED
            db.commit()
        return jsonify({"message": "Student blacklisted!"}), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500

 # ------------------------------- APPLICATIONS ------------------------------- #

@admin.get("/applications")
def get_all_applications():
    try:
        query = request.args.get("q", "").strip()
        with SessionLocal() as db:
            stmt = (
                select(Application)
                .options(
                    joinedload(Application.student),
                    joinedload(Application.job).joinedload(Job.company)
                )
                .join(StudentProfile)
                .outerjoin(Job)
            )
            
            if query:
                stmt = stmt.where(Job.title.like(f"{query}%"))
                
            applications = db.scalars(stmt).all()
            applications_data = [
                AdminApplicationResponse.model_validate(app).model_dump(mode="json")
                for app in applications
            ]
            
            response_json = json.dumps(applications_data)
            
        return Response(response_json, mimetype="application/json"), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# ------------------------------ EXTRA FEATURES ------------------------------ #

@admin.get("/count")
def get_count():
    try:
        with SessionLocal() as db:
            companies_count = db.scalars(
                select(func.count(CompanyProfile.id.distinct()))
            ).first()
            students_count = db.scalars(
                select(func.count(StudentProfile.id.distinct()))
            ).first()
            jobs_count = db.scalars(select(func.count(Job.id.distinct()))).first()
            current_app.logger.debug(f"Companies->{companies_count}")
            current_app.logger.debug(f"Students->{students_count}")
            current_app.logger.debug(f"Jobs->{jobs_count}")
        return jsonify(
            {
                "companies": companies_count,
                "students": students_count,
                "jobs": jobs_count,
            }
        ), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500