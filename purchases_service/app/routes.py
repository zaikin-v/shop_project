from app.models import User, Check, Purchase
from app.schemas import user_schema, users_schema, purchases_schema, check_schema
from app.validation import CreateCheckSchema
from app import db
from flask import Blueprint, jsonify
from webargs import fields
from webargs.flaskparser import use_args
from sqlalchemy.exc import IntegrityError

bp = Blueprint("purchases", __name__)


@bp.route("/user/create", methods=["POST"])
@use_args({"username": fields.String(required=True)}, location="json")
def add_user(args):
    try:
        user = User(username=args["username"])
        db.session.add(user)
        db.session.commit()
        return user_schema.dump(user)
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username blocked"}), 400


@bp.route("/user/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = User.query.get(user_id)
    if user is not None:
        return user_schema.dump(user)
    else:
        return jsonify({"message": "User not found"}), 404


@bp.route("/user/", methods=["GET"])
def get_all_user():
    users = User.query.all()
    return jsonify(users=users_schema.dump(users)), 200


@bp.route("/user/<int:user_id>/check/buy/", methods=["POST"])
@use_args(CreateCheckSchema)
def add_check(args, user_id):
    user = User.query.get(user_id)
    if user is None:
        db.session.rollback()
        return jsonify(message="User not found"), 404
    check = check_schema.load(args)
    check.customer = user
    db.session.add(check)
    db.session.commit()
    return check_schema.dump(check)
