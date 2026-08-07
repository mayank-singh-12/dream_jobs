import os
from flask import Flask, send_from_directory
from sqlalchemy import select
from database import SessionLocal
from models import User
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from routes.auth import auth
from routes.admin import admin
from routes.user import user
from routes.company import company
from routes.student import student

from sqlalchemy.orm import joinedload

app = Flask(__name__)
cors=CORS()
jwt=JWTManager()

app.config["SECRET_KEY"] = (
    "8c07948d2bbebb59bb5c55e7221ebddc621074c72448e81259bd7c6d332839ad"
)
app.config["JWT_SECRET_KEY"] = (
    "73938552ddc7b76be22a0f3d9e058d1cebe5fc2234dbe1e81da4c7ff74e5e900"
)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
app.config["JWT_TOKEN_LOCATION"] = ["headers"]


jwt.init_app(app)
cors.init_app(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    app.logger.debug(f"USER LOGGED IN --------------> \n {user}")
    return str(user.id)


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = int(jwt_data["sub"])
    with SessionLocal() as db:
        return db.scalars(
            select(User)
            .options(joinedload(User.company_profile), joinedload(User.student_profile))
            .where(User.id == identity)
        ).one_or_none()

@app.route('/uploads/<path:filename>')
def serve_uploads(filename):
    uploads_dir = os.path.join(app.root_path, 'uploads')
    return send_from_directory(uploads_dir, filename)

app.register_blueprint(auth)
app.register_blueprint(admin)
app.register_blueprint(user)
app.register_blueprint(company)
app.register_blueprint(student)

if __name__ == "__main__":
    app.run(debug=True)
