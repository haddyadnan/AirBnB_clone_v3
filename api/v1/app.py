#!/usr/bin/python3
""" RESTful API"""

import os

from flask import Flask, jsonify, make_response
from flask_cors import CORS

from api.v1.views import app_views
from models import storage

app = Flask(__name__)
CORS(app, resources={r"/api/v1/*": {"origins": "0.0.0.0"}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(error):
    """teardown instance"""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """Display 404 error"""

    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":

    host = os.getenv("HBNB_API_HOST", "0.0.0.0")
    port = os.getenv("HBNB_API_PORT", "5000")

    app.run(host=host, port=port, threaded=True)
