#!/usr/bin/python3
"""
Route for users
"""

from flask import jsonify, request

from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects.
    """
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a User object.
    """
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User object.
    """
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(user)
    storage.save()
    return jsonify({})

@app_views.route('/users/<user_id>', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User object.
    """
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User object.
    """
    user = storage.get(User, user_id)
    if user is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at' or key == 'email':
            continue
        setattr(user, key, value)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 200
