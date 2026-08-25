from models import JobStatus, ApplicationStatus, Job, UserRole, CompanyProfile, Application, StudentProfile
from flask import current_app
from schema import ApplicationResponse, UserResponse, CompanyUpdateRequest, StudentResponse
from flask import Blueprint, request, jsonify, Response
import json
from database import SessionLocal
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from schema import JobRequest, JobResponse, CompanyStatus, JobResponseForCompany
from flask_jwt_extended import jwt_required, current_user, verify_jwt_in_request
from pydantic import ValidationError

company = Blueprint("company",__name__,url_prefix="/api/company")

@company.before_request
@jwt_required()
def only_companies():
    if request.method == "OPTIONS":
        return

    verify_jwt_in_request()

    if current_user.role != UserRole.COMPANY:
        return (
            jsonify({"message": "You are not allowed to access this route."}),
            403,
        )

    if request.endpoint in ["company.get_details", "company.update_profile"]:
        return
    
    company_profile = current_user.company_profile
        
    if not company_profile or company_profile.status != CompanyStatus.APPROVED:
        return jsonify({"message": "Only approved companies are allowed to post placement drives/jobs."}), 403

# ------------------------------ Company Details ----------------------------- #

@company.get("/details")
def get_details():
    try:
        if current_user.company_profile is None:
            return jsonify({"message": "Company profile does not exist."}), 404

        user_data = UserResponse.model_validate(current_user).model_dump()
        response_json = json.dumps({"data": user_data})
        
        return Response(response_json, mimetype="application/json"), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500     

@company.patch("/profile")
def update_profile():
    try:
        data = request.get_json()
        validated_data = CompanyUpdateRequest.model_validate(data)
        update_data = validated_data.model_dump(exclude_unset=True)

        if not update_data:
            return jsonify({"message": "No fields to update."}), 400

        with SessionLocal() as db:
            company_profile = db.get(CompanyProfile, current_user.company_profile.id)
            if company_profile is None:
                return jsonify({"message": "Company profile does not exist."}), 404
            
            for key, value in update_data.items():
                setattr(company_profile, key, value)
            
            db.commit()
            
        return jsonify({"message": "Profile updated successfully!"}), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# ------------------------------ Placement Drive ----------------------------- #

# create a new placement drive
@company.post("/jobs")
def create_new_job():
    try:
        data = request.get_json()
        validated_data = JobRequest.model_validate(data)
        with SessionLocal() as db:
            new_job = Job(
                company_id=current_user.company_profile.id,
                **validated_data.model_dump(exclude={"company_id"})
            )
            db.add(new_job)
            db.commit()
            db.refresh(new_job)
            job_data = JobResponse.model_validate(new_job).model_dump()
        return jsonify({"message": "New Job created successfully!", "job": job_data}), 201
    
    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# get all the placement drives
@company.get("/jobs")
def get_company_jobs():
    try:
        company_profile = current_user.company_profile
        if not company_profile:
            return jsonify({"message": "Company profile not found."}), 404

        status = request.args.get("status") or request.args.get("job_status")

        with SessionLocal() as db:
            stmt = (
                select(Job, func.count(Application.id).label("application_count"))
                .outerjoin(Application, Job.id == Application.job_id)
                .where(Job.company_id == company_profile.id)
            )
            
            if status:
                try:
                    status_enum = JobStatus(status)
                except ValueError:
                    return jsonify({"message": f"Invalid job status '{status}'"}), 400
                stmt = stmt.where(Job.job_status == status_enum)
                
            stmt = stmt.group_by(Job.id)
            results = db.execute(stmt).all()
            
            jobs_data = []
            for job, count in results:
                job.application_count = count
                jobs_data.append(JobResponseForCompany.model_validate(job).model_dump())
        
        response_data = jsonify({"jobs": jobs_data})
        return response_data, 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# get details of a specific placement drive
@company.get("/jobs/<int:job_id>")
def get_company_job_detail(job_id):
    try:
        company_profile = current_user.company_profile
        if not company_profile:
            return jsonify({"message": "Company profile not found."}), 404

        with SessionLocal() as db:
            stmt = (
                select(Job, func.count(Application.id).label("application_count"))
                .outerjoin(Application, Job.id == Application.job_id)
                .where(Job.id == job_id, Job.company_id == company_profile.id)
                .group_by(Job.id)
            )
            result = db.execute(stmt).one_or_none()
            if not result:
                return jsonify({"message": "Placement drive not found or unauthorized."}), 404
            
            job, count = result
            job.application_count = count
            job_data = JobResponseForCompany.model_validate(job).model_dump(mode="json")
            
        response_data = json.dumps({"job": job_data})
        return Response(response_data, mimetype="application/json"),200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# close a placement drive
@company.post("/jobs/<int:job_id>/close")
def close_job(job_id):
    try:
        with SessionLocal() as db:
            stmt=select(Job).where(Job.id==job_id)
            job = db.scalars(stmt).one_or_none()
            if job is None:
                return jsonify({"message": "Job no longer exists."}), 404
            if job.job_status == JobStatus.CLOSED:
                return jsonify({"message": "job is already closed."}), 400
            job.job_status=JobStatus.CLOSED
            db.commit()
        return jsonify({"message":"Placement drive closed!"}),200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500


# -------------------------------- Application ------------------------------- #

# applications for specific placement drive
@company.get("/applications/<int:job_id>")
def get_job_applications(job_id):
    try:
        with SessionLocal() as db:
            stmt=select(Application).where(Application.job_id==job_id)
            applications = db.scalars(stmt).all()
            applications_data = [ApplicationResponse.model_validate(application).model_dump() for application in applications]
            current_app.logger.debug(applications_data)
        return jsonify({"applications":applications_data}),200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500

# view a specific application with full student data
@company.get("/applications/details/<int:application_id>")
def get_application_details(application_id):
    try:
        with SessionLocal() as db:
            stmt = (
                select(Application)
                .options(
                    joinedload(Application.student).joinedload(StudentProfile.user),
                    joinedload(Application.job).joinedload(Job.company)
                )
                .where(Application.id == application_id)
            )
            application = db.scalars(stmt).one_or_none()
            
            if application is None:
                return jsonify({"message": "Application does not exist."}), 404
            
            if application.job is None or application.job.company_id != current_user.company_profile.id:
                return jsonify({"message": "You are not authorized to view this application."}), 403
            
            application_data = ApplicationResponse.model_validate(application).model_dump(mode="json")
            
            student_data = StudentResponse.model_validate(application.student.user).model_dump(mode="json")
            application_data["student_details"] = student_data

            job_data = JobResponse.model_validate(application.job).model_dump(mode="json")
            application_data["job_details"] = job_data
            
            response_json = json.dumps({"application": application_data})
            
        return Response(response_json, mimetype="application/json"), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500

# shortlist application
@company.post("/applications/<int:application_id>/shortlist")
def shorlist_application(application_id):
    try:
        with SessionLocal() as db:
            stmt = select(Application).where(Application.id==application_id)
            application = db.scalars(stmt).one_or_none()
            if application is None:
                return jsonify({"message": "Application no longer exists."}), 404
            if application.status == ApplicationStatus.SHORTLISTED:
                return jsonify({"message": "Application is already shortlisted."}), 400
            application.status=ApplicationStatus.SHORTLISTED
            db.commit()
        return jsonify({"message":"Application shortlisted!"}),200
        
    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500

# approve application
@company.post("/applications/<int:application_id>/approve")
def approve_application(application_id):
    try:
        with SessionLocal() as db:
            stmt = select(Application).where(Application.id==application_id)
            application = db.scalars(stmt).one_or_none()
            if application is None:
                return jsonify({"message": "Application no longer exists."}), 404
            if application.status == ApplicationStatus.APPROVED:
                return jsonify({"message": "Application is already approved."}), 400
            application.status=ApplicationStatus.APPROVED
            db.commit()
        return jsonify({"message":"Application approved!"}),200
        
    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500

# pending application
@company.post("/applications/<int:application_id>/pending")
def pending_application(application_id):
    try:
        with SessionLocal() as db:
            stmt = select(Application).where(Application.id==application_id)
            application = db.scalars(stmt).one_or_none()
            if application is None:
                return jsonify({"message": "Application no longer exists."}), 404
            if application.status == ApplicationStatus.PENDING:
                return jsonify({"message": "Application is already pending."}), 400
            application.status=ApplicationStatus.PENDING
            db.commit()
        return jsonify({"message":"Application pending!"}),200
        
    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500

# reject application
@company.post("/applications/<int:application_id>/reject")
def reject_application(application_id):
    try:
        with SessionLocal() as db:
            stmt = select(Application).where(Application.id==application_id)
            application = db.scalars(stmt).one_or_none()
            if application is None:
                return jsonify({"message": "Application no longer exists."}), 404
            if application.status == ApplicationStatus.REJECTED:
                return jsonify({"message": "Application is already rejected."}), 400
            application.status=ApplicationStatus.REJECTED
            db.commit()
        return jsonify({"message":"Application rejected!"}),200
        
    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500

