#!/usr/bin/python3

""" View for State objects """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    """
    Retrieves the list of all State objects:
    """
    states = storage.all(State)
    states_list = [state.to_dict() for state in states.values()]
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def one_state(state_id):
    """
    Retrieves a State object
    """
    state_dict = storage.get(State, state_id)
    if state_dict is None:
        abort(404)
    return jsonify(state_dict.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"])
def delete_state(state_id):
    """
    Deletes a State object
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    create new state object
    """

    if not request.get_json():
        abort(400, description="Not a json")
    state_info = request.get_json()
    if state_info.get("name", None) is None:
        abort(400, description="Missing name")

    state = State(**state_info)
    state.save()

    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """update state object"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(404, description="Not a JSON")

    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(state, k, v)
    return make_response(jsonify(state.to_dict()), 200)
