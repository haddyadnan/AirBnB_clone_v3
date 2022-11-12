#!/usr/bin/python3

""" index file """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.user import User
from models.place import Place
from models.city import City
from models.review import Review


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
