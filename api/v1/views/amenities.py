#!/usr/bin/python3

""" View for City objects """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenity():
    """
    Retrieves the list of all Amenity objects:
    """
    amenities = storage.all(Amenity)

    amenity_list = [am.to_dict() for am in amenities.values()]
    return jsonify(amenity_list)


@app_views.route("/amenities/<am_id>", methods=["GET"], strict_slashes=False)
def one_amenity(am_id):
    """
    Retrieves an Amenity object
    """
    amenity_dict = storage.get(Amenity, am_id)
    if amenity_dict is None:
        abort(404)
    return jsonify(amenity_dict.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"])
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    create new Amenity object
    """

    if not request.get_json():
        abort(400, description="Not a json")
    data = request.get_json()
    if data.get("name", None) is None:
        abort(400, description="Missing name")

    amenity = Amenity(**data)
    amenity.save()

    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route("/amenities/<am_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(am_id):
    """update Amenity object"""
    amenity = storage.get(Amenity, am_id)

    if not amenity:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
