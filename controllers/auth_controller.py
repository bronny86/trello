from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

from init import bcrypt, db
from models.user import User, user_schema

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["POST"])
def register_user():

    try:
        # get the data from the body of the request
        body_data = request.get_json()
        # create an instance of the user model
        user = User(
            name=body_data.get("name"),
            email=body_data.get("email")
            )
        # extract the passwortd from the body
        password = body_data.get("password")
        # hash the password as well
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        # add and commit to the DB
        db.session.add(user)
        db.session.commit()

        # respond back to the front end
        return user_schema.dump(user), 201
    
    except IntegrityError as err:
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            return {"error": f"The column {err.orig.diag.column_name} is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            # unique violation
            return {"error": "Email address is already is use"}, 409