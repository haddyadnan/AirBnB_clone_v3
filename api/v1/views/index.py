#!/usr/bin/python3

""" index file """

from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """returns status"""

    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """
    An endpoint that retrieves
    the number of each objects by type
    """
    counts = {}
    classes = {
        Amenity: "amenities",
        City: "cities",
        Place: "places",
        Review: "reviews",
        State: "states",
        User: "users",
    }
    for c, name in classes.items():
        counts[name] = storage.count(c)
    return jsonify(counts)
