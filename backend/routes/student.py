from dns import zonefile
import os
from sqlalchemy.orm import joinedload
from flask import Response
from sqlalchemy import or_
from models import User
from models import CompanyProfile, StudentProfile
import json
from flask import Flask, Blueprint, request, jsonify, current_app
from database import SessionLocal
from sqlalchemy import select, text
from models import Job,UserRole,Application, JobStatus
from schema import JobRequest, JobResponse, CompanyStatus, CompanyResponseForStudent, ApplicationResponse, UserResponse, StudentUpdateRequest, StudentApplicationResponse, ApplicationRequest, ValidateRegisteredCompany
from flask_jwt_extended import jwt_required, current_user, verify_jwt_in_request
from pydantic import ValidationError

student = Blueprint("student",__name__,url_prefix="/api/student")

@student.before_request
@jwt_required()
def only_students():
    if request.method == "OPTIONS":
        return

    verify_jwt_in_request()

    if current_user.role != UserRole.STUDENT:
        return (
            jsonify({"message": "You are not allowed to access this route."}),
            403,
        )

# ------------------------------ Student Details ----------------------------- #
# get student details
@student.get("/details")
def get_details():
    try:
        if current_user.student_profile is None:
            return jsonify({"message": "Student profile does not exist."}), 404
        
        user_data = UserResponse.model_validate(current_user).model_dump(mode="json")
        response_json = json.dumps({"data": user_data})
        
        return Response(response_json, mimetype="application/json"), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# update student details 
@student.patch("/profile")
def update_profile():
    try:
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
            data = {k: v for k, v in data.items() if v != ""}
            
        validated_data = StudentUpdateRequest.model_validate(data)
        update_data = validated_data.model_dump(exclude_unset=True)

        if "cv" in request.files:
            file = request.files["cv"]
            if file.filename != "":
                if file and allowed_file(file.filename):
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    filename = f"student_{current_user.student_profile.id}.pdf"
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    update_data["resume_path"] = f"uploads/cvs/{filename}"
                else:
                    return jsonify({"message": "Invalid file type. Only PDF is allowed."}), 400

        if not update_data:
            return jsonify({"message": "No fields to update."}), 400

        with SessionLocal() as db:
            student_profile = db.get(StudentProfile, current_user.student_profile.id)
            if student_profile is None:
                return jsonify({"message": "Student profile does not exist."}), 404
            
            for key, value in update_data.items():
                setattr(student_profile, key, value)
            
            db.commit()
            
        return jsonify({"message": "Profile updated successfully!"}), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# ---------------------------------------------------------------------------- #

# get all companies
@student.get("/companies")
def get_all_companies():
    try:
        query = request.args.get("q", "").strip()
        current_app.logger.debug(query)

        with SessionLocal() as db:
            stmt = (
                select(CompanyProfile)
                .join(User, User.id == CompanyProfile.user_id)
                .join(Job, CompanyProfile.id == Job.company_id)
                .where(
                    User.role == UserRole.COMPANY,
                    CompanyProfile.status == CompanyStatus.APPROVED,
                    Job.job_status == JobStatus.APPROVED
                )
                .distinct()
            )
            if query:
                stmt = stmt.where(
                    or_(
                        CompanyProfile.name.like(f"{query}%"),
                        CompanyProfile.location.like(f"{query}%")
                    )
                )
            companies = db.scalars(stmt).all()
            current_app.logger.debug(f"\n-----companies-----{companies}\n")
            companies_data = [
                ValidateRegisteredCompany.model_validate(company).model_dump(mode="json")
                for company in companies
            ]
            response_data = json.dumps({"companies":companies_data})
        return Response(response_data, mimetype="application/json"),200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# get all open jobs
@student.get("/jobs")
def get_all_jobs():
    try:
        query=request.args.get("q","").strip()
        query_job_type=request.args.get("t","").strip()

        with SessionLocal() as db:
            stmt = select(Job).join(CompanyProfile).where(Job.job_status==JobStatus.APPROVED)
            if query_job_type:
                stmt = stmt.where(
                    Job.job_type==query_job_type
                )
            if query:
                stmt = stmt.where(or_(
                    Job.title.like(f"{query}%"),
                    Job.location.like(f"{query}%")
                ))
            jobs = db.scalars(stmt).all()
            jobs_data = [JobResponse.model_validate(job).model_dump(mode="json") for job in jobs]
            response_data = json.dumps({"jobs":jobs_data})
        return Response(response_data,mimetype="application/json"),200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:  
        return jsonify({"message": str(e)}), 500

# get single job with full company details
@student.get("/jobs/<int:job_id>")
def get_job_details(job_id):
    try:
        with SessionLocal() as db:
            stmt = (
                select(Job)
                .options(joinedload(Job.company))
                .where(Job.id == job_id, Job.job_status == JobStatus.APPROVED)
            )
            job = db.scalars(stmt).one_or_none()
            if job is None:
                return jsonify({"message": "Job does not exist or is not active."}), 404
            
            job_data = JobResponse.model_validate(job).model_dump(mode="json")
            response_json = json.dumps({"job": job_data})
            
        return Response(response_json, mimetype="application/json"), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# get open jobs offered by specific company id
@student.get("/companies/<int:company_id>/jobs")
def get_company_open_jobs(company_id):
    try:
        with SessionLocal() as db:
            company_check = db.get(CompanyProfile, company_id)
            if company_check is None:
                return jsonify({"message": "Company does not exist."}), 404

            stmt = (
                select(Job)
                .options(joinedload(Job.company))
                .where(Job.company_id == company_id, Job.job_status == JobStatus.APPROVED)
            )
            jobs = db.scalars(stmt).all()
            jobs_data = [JobResponse.model_validate(job).model_dump(mode="json") for job in jobs]
            response_json = json.dumps({"jobs": jobs_data})
            
        return Response(response_json, mimetype="application/json"), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500


# -------------------------------- Application ------------------------------- #

# get all applications for jobs that are currently open (approved)
@student.get("/applications/open")
def get_open_job_applications():
    try:
        if current_user.student_profile is None:
            return jsonify({"message": "Student profile does not exist."}), 404

        with SessionLocal() as db:
            stmt = (
                select(Application)
                .join(Job, Application.job_id == Job.id)
                .options(joinedload(Application.job).joinedload(Job.company))
                .where(
                    Application.student_id == current_user.student_profile.id,
                    Job.job_status == JobStatus.APPROVED
                )
            )
            applications = db.scalars(stmt).all()
            applications_data = [
                StudentApplicationResponse.model_validate(app).model_dump(mode="json")
                for app in applications
            ]
            response_json = json.dumps({"applications": applications_data})

        return Response(response_json, mimetype="application/json"), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# get all applications
@student.get("/applications")
def get_all_applications():
    try:
        if current_user.student_profile is None:
            return jsonify({"message": "Student profile does not exist."}), 404

        with SessionLocal() as db:
            stmt = (
                select(Application)
                .options(joinedload(Application.job).joinedload(Job.company))
                .where(Application.student_id == current_user.student_profile.id)
            )
            applications = db.scalars(stmt).all()
            
            applications_data = [
                StudentApplicationResponse.model_validate(app).model_dump(mode="json")
                for app in applications
            ]
                
            response_json = json.dumps({"applications": applications_data})
            
        return Response(response_json, mimetype="application/json"), 200

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

# submit application for a job
@student.post("/applications")
def apply_to_job():
    try:
        data = request.get_json()
        validated_data = ApplicationRequest.model_validate(data)
        
        if current_user.student_profile is None:
            return jsonify({"message": "Student profile does not exist."}), 404

        with SessionLocal() as db:
            job = db.get(Job, validated_data.job_id)
            if job is None:
                return jsonify({"message": "Job does not exist."}), 404
            
            if job.job_status != JobStatus.APPROVED:
                return jsonify({"message": "This job is not accepting applications."}), 400

            if job.required_cgpa is not None:
                if current_user.student_profile.cgpa < job.required_cgpa:
                    return jsonify({
                        "message": f"Your CGPA ({current_user.student_profile.cgpa}) does not meet the minimum requirement ({job.required_cgpa}) for this job."
                    }), 400

            stmt = select(Application).where(
                Application.student_id == current_user.student_profile.id,
                Application.job_id == validated_data.job_id
            )
            existing_app = db.scalars(stmt).one_or_none()
            if existing_app is not None:
                return jsonify({"message": "You have already applied to this job."}), 400

            new_application = Application(
                student_id=current_user.student_profile.id,
                job_id=validated_data.job_id
            )
            db.add(new_application)
            db.commit()
            
        return jsonify({"message": "Successfully applied to the job!"}), 201

    except ValidationError as ve:
        return jsonify({"message": str(ve)}), 400

    except Exception as e:
        return jsonify({"message": str(e)}), 500

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "cvs")
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@student.post("/upload-cv")
def upload_cv():
    try:
        if current_user.student_profile is None:
            return jsonify({"message": "Student profile does not exist."}), 404

        if "cv" not in request.files:
            return jsonify({"message": "No file part in the request under the key 'cv'."}), 400
        
        file = request.files["cv"]
        if file.filename == "":
            return jsonify({"message": "No file selected."}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"message": "Invalid file type. Only PDF is allowed."}), 400

        file_bytes = file.read()
        storage_path = f"cv_{current_user.student_profile.id}.pdf"

        from app import supabase
        response = supabase.storage.from_('dream_jobs_cv').upload(
            path=storage_path,
            file=file_bytes,
            file_options={'upsert':'true'}
        )

        public_url = supabase.storage.from_('dream_jobs_cv').get_public_url(storage_path)

        with SessionLocal() as db:
            student_profile = db.get(StudentProfile, current_user.student_profile.id)
            if not student_profile:
                return jsonify({"message": "Student doesn't exist."}), 400

            student_profile.resume_path = public_url
            db.commit()

        return jsonify({"message": "CV uploaded successfully!", "resume_path": public_url}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": str(e)}), 500
