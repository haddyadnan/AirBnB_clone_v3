#!/usr/bin/python3

""" View for City objects """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def all_user():
    """
    Retrieves the list of all User objects:
    """
    users = storage.all(User)

    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def one_user(user_id):
    """
    Retrieves an User object
    """
    user_dict = storage.get(User, user_id)
    if user_dict is None:
        abort(404)
    return jsonify(user_dict.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """
    Deletes a User object
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    create new User object
    """

    if not request.get_json():
        abort(400, description="Not a json")
    data = request.get_json()
    if data.get("name", None) is None:
        abort(400, description="Missing name")

    user = User(**data)
    user.save()

    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """update User object"""
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(user, k, v)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
