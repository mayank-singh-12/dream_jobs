import json
from flask import Flask, request, jsonify,current_app
from sqlalchemy import select, text
from database import SessionLocal
from models import Base, User, Job, UserRole, StudentProfile, CompanyProfile
from schema import (
    LoginRequest,
    RegisterStudentRequest,
    RegisterCompanyRequest,
    # Student Schemas
    StudentResponse,
    # Company Schemas
    CompanyResponse,
)

from pydantic import ValidationError
from flask_jwt_extended import (
    create_access_token
)
import os

from flask import Blueprint

auth = Blueprint("auth",__name__, url_prefix="/api")

def create_base_user(validated_data, role):
    user_fields = {
        "username": validated_data["username"],
        "email": validated_data["email"],
        "password": validated_data["password"],
        "role": role,
    }
    return User(**user_fields)

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads", "cvs")
ALLOWED_EXTENSIONS = {"pdf"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@auth.post("/register/student")
def register_student():
    try:
        data = request.form.to_dict()
        print(data)
        validated_data = RegisterStudentRequest.model_validate(data).model_dump()

        if "cv" not in request.files:
            return jsonify({"message": "CV file upload is required during registration."}), 400

        file = request.files["cv"]
        if file.filename == "":
            return jsonify({"message": "No file selected."}), 400

        if not allowed_file(file.filename):
            return jsonify({"message": "Invalid file type. Only PDF is allowed."}), 400

        with SessionLocal() as db:
            new_user = create_base_user(validated_data, UserRole.STUDENT)

            student_profile = StudentProfile(
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                school=validated_data["school"],
                cgpa=validated_data["cgpa"],
                phone_number=validated_data["phone_number"],
            )
            new_user.student_profile = student_profile

            db.add(new_user)
            db.flush()

            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = f"student_{student_profile.id}.pdf"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            student_profile.resume_path = f"uploads/cvs/{filename}"
            db.commit()
            db.refresh(new_user)
            current_app.logger.debug(f"NEW USER -------------> \n {new_user}")
            response = StudentResponse.model_validate(new_user).model_dump()
        return jsonify({"message": "Student registered successfully!", "user": response}), 201
    
    except ValidationError as ve:
        current_app.logger.error(ve)
        return jsonify({"message": ve.errors()}), 400
    
    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500

@auth.post("/register/company")
def register_company():
    try:
        data = request.get_json()
        validated_data = RegisterCompanyRequest.model_validate(data).model_dump()

        with SessionLocal() as db:
            new_user = create_base_user(validated_data, UserRole.COMPANY)

            company_profile = CompanyProfile(
                name=validated_data["name"],
                website=validated_data["website"],
                about=validated_data["about"],
                location=validated_data["location"],
            )
            new_user.company_profile = company_profile

            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            response = CompanyResponse.model_validate(new_user).model_dump()
        return jsonify({"message": "Company registered!", "user": response}), 201
    
    except ValidationError as ve:
        current_app.logger.error(ve)
        return jsonify({"message": ve.errors()}), 400

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500

@auth.post("/login")
def login():
    try:
        data = request.get_json()
        validated_data = LoginRequest.model_validate(data).model_dump()
        current_app.logger.debug(validated_data)

        with SessionLocal() as db:
            stmt = None

            if validated_data["username"] is not None:
                stmt = select(User).where(User.username == validated_data["username"])
                current_app.logger.info(f"USERNAME STATEMENT -> {stmt}")

            if validated_data["email"] is not None:
                stmt = select(User).where(User.email == validated_data["email"])
                current_app.logger.info(f"EMAIL STATEMENT -> {stmt}")

            if stmt is None:
                return (
                    jsonify({"message": "Either username or email must be provided."}),
                    400,
                )

            user = db.scalars(stmt).first()

            if not user:
                return jsonify({"message": "Invalid username/email."}), 404

            if validated_data["password"] != user.password:
                return jsonify({"message": "Invalid password."}), 400

            access_token = create_access_token(identity=user)

            response = jsonify({
                "message": "log in success!",
                "token": access_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "role": user.role.value
                }
            })

        return response, 200

    except ValidationError as ve:
        return jsonify({"message": json.loads(ve.json())}), 400

    except Exception as e:
        current_app.logger.error(e)
        return jsonify({"message": str(e)}), 500