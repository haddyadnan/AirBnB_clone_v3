#!/usr/bin/python3

""" View for City objects """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def one_City(city_id):
    """
    Retrieves a City object
    """
    city_dict = storage.get(City, city_id)
    if city_dict is None:
        abort(404)
    return jsonify(city_dict.to_dict())


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def all_cities(state_id):
    """
    Retrieves the list of all City objects:
    """
    states = storage.get(State, state_id)
    if not states:
        abort(404)
    cities_list = [city.to_dict() for city in states.cities]
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_City(city_id):
    """
    Deletes a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_City(state_id):
    """
    create new City object
    """

    if not request.get_json():
        abort(400, description="Not a json")
    data = request.get_json()
    if data.get("name", None) is None:
        abort(400, description="Missing name")

    state = storage.get(State, state_id)
    if not state:
        abort(404)
    city = City(**data)
    city.state_id = state.id
    city.save()

    return make_response(jsonify(city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_City(city_id):
    """update City object"""
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, k, v)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
