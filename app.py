import json
from flask import Flask, request, jsonify
from sqlalchemy import select, text
from database import SessionLocal
from models import Base, User, Job, Institute, UserRole, StudentProfile, CompanyProfile
from schema import (
    UserRequest,
    UserResponse,
    UserUpdateRequest,
    JobRequest,
    JobResponse,
    LoginRequest,
    # Auth Schemas
    RegisterUserBase,
    RegisterUserRequest,
    RegisterUserResponse,
    RegisterStudentRequest,
    RegisterCompanyRequest
)
from pydantic import ValidationError
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    get_jwt_identity,
    jwt_required,
    current_user,
    set_access_cookies,
)
import datetime

from database import engine

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    "8c07948d2bbebb59bb5c55e7221ebddc621074c72448e81259bd7c6d332839ad"
)
app.config["JWT_SECRET_KEY"] = (
    "73938552ddc7b76be22a0f3d9e058d1cebe5fc2234dbe1e81da4c7ff74e5e900"
)
# app.config["JWT_ACCESS_TOKEN_EXPIRES"] = datetime.timedelta(hours=2)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SAMESITE"] = "None"
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_COOKIE_CSRF_PROTECT"] = False

CORS(app, supports_credentials=True)

jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    with SessionLocal() as db:
        return db.scalars(select(User).where(User.id == identity)).one_or_none()


@app.get("/")
def home():
    return "Welcome to Flask."


# ---------------------------------------------------------------------------- #
#                                  AUTH ROUTES                                 #
# ---------------------------------------------------------------------------- #


@app.post("/register")
def register():
    try:
        data = request.get_json()
        role = data.get("role", UserRole.STUDENT.value)

        if role == UserRole.STUDENT.value:
            # app.logger.debug("Hi here")
            # app.logger.info(f"UNVALIDATED DATA : {data}")
            validated_data = RegisterStudentRequest.model_validate(data).model_dump()

        elif role == UserRole.COMPANY.value:
            validated_data = RegisterCompanyRequest.model_validate(data).model_dump()

        else:
            return jsonify({"error": "Invalid role provided."}), 400

        app.logger.info(f"VALIDATED DATA : {validated_data}")

        with SessionLocal() as db:

            user_fields = {
                k: v
                for k, v in validated_data.items()
                if k in User.__table__.columns.keys()
            }

            if validated_data["role"] == UserRole.STUDENT.value:
                student_fields = {
                    k: v
                    for k, v in validated_data.items()
                    if k in StudentProfile.__table__.columns.keys()
                }
                new_student_profile = StudentProfile(**student_fields)
                new_user = User(**user_fields, student_profile=new_student_profile)

            if validated_data["role"] == UserRole.COMPANY.value:
                company_fields = {
                    k: v
                    for k, v in validated_data.items()
                    if k in CompanyProfile.__table__.columns.keys()
                }
                new_company_profile = CompanyProfile(**company_fields)
                new_user = User(**user_fields, company_profile=new_company_profile)

            app.logger.info(f"USER_INFO -> {
                new_user.student_profile.__repr__()
                if new_user.student_profile
                else new_user.company_profile.__repr__()}")

            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            validated_response = RegisterUserResponse.model_validate(new_user).model_dump()
            app.logger.info(f"VALIDATED RESPONSE -> {validated_response}")

        return (
            jsonify(
                {"message": "User registered successfully!", "user_detail": validated_response}
            ),
            201,
        )

        # return (
        #     jsonify(
        #         {"message": "User registered successfully!"}
        #     ),
        #     201,
        # )

    except ValidationError as ve:
        return jsonify({"error": json.loads(ve.json())}), 400

    except Exception as e:
        app.logger.error(e)
        return jsonify({"error": str(e)}), 500


@app.post("/login")
def login():
    try:
        data = request.get_json()
        validated_data = LoginRequest.model_validate(data).model_dump()
        app.logger.debug(validated_data)

        with SessionLocal() as db:

            if validated_data["username"] is not None:
                stmt = select(User).where(User.username == validated_data["username"])
                app.logger.info(f"USERNAME STATEMENT -> {stmt}")

            if validated_data["email"] is not None:

                stmt = select(User).where(User.email == validated_data["email"])
                app.logger.info(f"EMAIL STATEMENT -> {stmt}")

            user = db.scalars(stmt).first()

            if not user:
                return jsonify({"error": "Invalid username/email."}), 404

            if validated_data["password"] != user.password:
                return jsonify({"error": "Invalid password."}), 400

            access_token = create_access_token(identity=user)

            response = jsonify({"message": "log in success!"})

            set_access_cookies(response, access_token)
        return response, 200

    except ValidationError as ve:
        return jsonify({"error": json.loads(ve.json())}), 400

    except Exception as e:
        Print("GENERIC", e)
        return jsonify({"error": str(e)}), 500

# ------------------------------- ADMIN ROUTES ------------------------------- #

# ---------------------------------------------------------------------------- #
#                                  USER ROUTES                                 #
# ---------------------------------------------------------------------------- #


@app.get("/protected")
@jwt_required()
def protected_route():
    app.logger.debug(current_user)
    return jsonify({"username": current_user.username})


@app.get("/users")
@jwt_required()
def get_all_users():
    try:
        app.logger.debug(current_user)
        with SessionLocal() as db:
            stmt = select(User)
            users = db.scalars(stmt).all()
            app.logger.info(f"USERS -> {users[0]}")
            result = [UserResponse.model_validate(user).model_dump() for user in users]
        return jsonify({"users": result}), 200

    except Exception as e:
        app.logger.error(str(e))
        return jsonify({"error": str(e)}), 500


@app.post("/users")
@jwt_required()
def create_new_user():
    try:
        print(current_user)    
        data = request.get_json()
        validated_data = UserRequest.model_validate(data)

        with SessionLocal() as db:
            new_user = User(**validated_data.model_dump())
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            user_data = UserResponse.model_validate(new_user).model_dump()

        return jsonify({"message": "saved new user", "user": user_data}), 201

    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.patch("/users/<uuid:user_id>")
def edit_user(user_id):
    try:
        data = request.get_json()
        validated_data = UserUpdateRequest.model_validate(data)
        update_data = validated_data.model_dump(exclude_unset=True)

        with SessionLocal() as db:
            user = db.get(User, user_id)

            if not user:
                return jsonify({"error": "user not found."}), 404

            for key, value in update_data.items():
                setattr(user, key, value)

            db.commit()
            db.refresh(user)

        user_response = UserResponse.model_validate(user).model_dump()
        return (
            jsonify(
                {"message": "user updated successfully", "updated_user": user_response}
            ),
            200,
        )

    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.delete("/users/<uuid:user_id>")
def delete_user(user_id):
    try:
        with SessionLocal() as db:
            user = db.get(User, user_id)
            if not user:
                return jsonify({"error": "user not found."}), 404
            deleted_user = UserResponse.model_validate(user).model_dump()
            db.delete(user)
            db.commit()
        return (
            jsonify(
                {"message": "User deleted successfully!", "deleted_user": deleted_user}
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------------------------------------------------------- #
#                                  JOB ROUTES                                  #
# ---------------------------------------------------------------------------- #


@app.get("/jobs")
def get_all_jobs():
    try:
        with SessionLocal() as db:
            stmt = select(Job)
            jobs = db.scalars(stmt).all()
            validated_jobs = [
                JobResponse.model_validate(job).model_dump() for job in jobs
            ]
        return jsonify({"jobs": validated_jobs}), 200

    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.post("/jobs")
def new_job():
    try:
        data = request.get_json()
        validated_data = JobRequest.model_validate(data)

        with SessionLocal() as db:
            new_job = Job(**validated_data.model_dump())
            db.add(new_job)
            db.commit()
            db.refresh(new_job)

            job_data = JobResponse.model_validate(new_job).model_dump()

        return jsonify({"message": "New Job formed!", "job": job_data})

    except ValidationError as ve:
        return jsonify({"error": str(ve)}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

    #        /\
    #       /  \
    #      /    \
    #     |  |  |
    #     |  |  |
    #     |  |  |
    #     |  |  |
    #     |  |  |
    #     |  |  |
    #     |  |  |
    # TTTTTTTTTTTTTTTTT
    #      |   |
    #      |   |
    #      |   |
    #      |   |
    #      TTTTT       