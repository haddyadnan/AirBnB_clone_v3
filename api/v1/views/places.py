#!/usr/bin/python3

""" View for City objects """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<c_id>/places", methods=["GET"], strict_slashes=False)
def all_places(cid):
    """
    Retrieves the list of all Place objects:
    """
    cities = storage.get(City, cid)
    if not cities:
        abort(404)
    places_list = [place.to_dict() for place in cities.places]
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def one_place(place_id):
    """
    Retrieves a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """
    Deletes a Place object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<id>/places", methods=["POST"], strict_slashes=False)
def create_place(id):
    """
    create new place object
    id: city id
    """

    if not request.get_json():
        abort(400, description="Not a json")
    data = request.get_json()
    if data.get("user_id", None) is None:
        abort(400, description="Missing user_id")
    if data.get("name", None) is None:
        abort(400, description="Missing user_id")

    city = storage.get(City, id)
    if not city:
        abort(404)

    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    place = Place(**data)
    place.city_id = city.id
    place.save()

    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """update Place object"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
