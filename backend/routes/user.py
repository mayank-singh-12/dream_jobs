import json
from flask import Flask, request, jsonify,current_app
from sqlalchemy import select, text
from database import SessionLocal
from models import User
from schema import (
    UserRequest,
    UserResponse,
    UserUpdateRequest
)

from pydantic import ValidationError
from flask_jwt_extended import (
    jwt_required,
    current_user
)
import datetime

from flask import Blueprint

from database import engine

user = Blueprint("api/user",__name__)

@user.post("/users")
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


@user.patch("/users/<uuid:user_id>")
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


@user.delete("/users/<uuid:user_id>")
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
