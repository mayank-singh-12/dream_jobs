from flask import Flask, request, jsonify
from sqlalchemy import select, text
from database import SessionLocal
from models import Base, User, Job, Institute
from schema import UserRequest, UserResponse, UserUpdateRequest, JobRequest, JobResponse
from pydantic import ValidationError

from database import engine

app = Flask(__name__)


@app.get("/")
def home():
    return "Welcome to Flask."


# ---------------------------------------------------------------------------- #
#                                  USER ROUTES                                 #
# ---------------------------------------------------------------------------- #


@app.get("/users")
def get_all_users():
    try:
        with SessionLocal() as db:
            stmt = select(User)
            users = db.scalars(stmt).all()
            result = [UserResponse.model_validate(user).model_dump() for user in users]
        return jsonify({"users": result}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@app.post("/users")
def create_new_user():
    try:
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


# def main():
#     # Open a session
#     db = SessionLocal()

#     try:
#         # Example 1: Create a user
#         print("Creating a new user...")
#         new_user = User(
#             username="alice", email="alice@example.com", password="securepassword123"
#         )
#         db.add(new_user)
#         db.commit()  # Save to the database
#         db.refresh(new_user)  # Get the newly generated ID back from the DB
#         print(f"Created: {new_user}")

#         # Example 2: Read users
#         print("\nQuerying all users...")
#         # SQLAlchemy 2.0 uses select() and session.scalars()
#         stmt = select(User)
#         users = db.scalars(stmt).all()
#         for u in users:
#             print(f"- {u}")

#         # Example 3: Update a user
#         print("\nUpdating user...")
#         stmt = select(User).where(User.username == "alice")
#         user_to_update = db.scalars(stmt).first()
#         if user_to_update:
#             user_to_update.email = "alice_new@example.com"
#             db.commit()
#             print("Updated user email!")

#         # Example 4: Delete a user
#         # print("\nDeleting user...")
#         # if user_to_update:
#         #     db.delete(user_to_update)
#         #     db.commit()
#         #     print("Deleted!")

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         print(
#             "Note: This script requires a running PostgreSQL database and run migrations via Alembic."
#         )
#     finally:
#         db.close()  # Always close the session when done!


if __name__ == "__main__":
    app.run(debug=True)
