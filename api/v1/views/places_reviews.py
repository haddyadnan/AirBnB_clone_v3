#!/usr/bin/python3

""" View for City objects """

from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<pid>/reviews", methods=["GET"], strict_slashes=False)
def all_reviews(pid):
    """
    Retrieves the list of all Review objects:
    """
    places = storage.get(Place, pid)

    if places is None:
        abort(404)

    review_list = [review.to_dict() for review in places.reviews]
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def one_review(review_id):
    """
    Retrieves a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"])
def delete_review(review_id):
    """
    Deletes a Review object
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<id>/reviews", methods=["POST"], strict_slashes=False)
def create_reveiw(id):
    """
    create new place object
    id: place_id
    """

    if not request.get_json():
        abort(400, description="Not a json")

    data = request.get_json()
    if data.get("user_id", None) is None:
        abort(400, description="Missing user_id")

    if data.get("text", None) is None:
        abort(400, description="Missing text")

    place = storage.get(Place, id)
    if not place:
        abort(404)

    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    review = Review(**data)
    review.place_id = place.id
    review.save()

    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """update Review object"""
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    for k, v in request.get_json().items():
        if k not in ["id", "created_at", "updated_at", "user_id", "place_id"]:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
