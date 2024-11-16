#!/usr/bin/python3
"""
starts a Flask web application
"""

import os
from flask import Flask, jsonify


from models import storage
from api.v1.views import app_views

host = os.getenv("HBNB_API_HOST", "0.0.0.0")
port = os.getenv("HBNB_API_PORT", 5000)


app = Flask(__name__)


app.register_blueprint(app_views)



@app.errorhandler(404)
def errorhandler(e):
    """Error handler. Return JSON for 404 errors
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(405)
def not_allowed_method(e):
    """Error handler. Return JSON for 405 errors
    """
    return jsonify({"error": "Method not allowed"}), 405

@app.teardown_appcontext
def close_storage(exception):
    """closes the storage on teardown"""
    storage.close()


if __name__ == "__main__":
    app.run(host=host,
            port=port,
            threaded=True,
            debug=True)
