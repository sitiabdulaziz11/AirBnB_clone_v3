#!/usr/bin/python3
""""
Route for amenities
"""

from flask import jsonify, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects.
    """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """ Retrieves a specific Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object.
    """
    if not amenity_id:
        return jsonify({"error": "To Delete Amenity ID is required"}), 400
    
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Method to create a new Amenity.
    """
    data = request.get_json()
    
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Method to update a Amenity.
    """
    amenity = storage.get(Amenity, amenity_id)
    print(amenity)
    if amenity is None:
        return jsonify({"error": "Not found"}), 404
    
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    
    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue
        setattr(amenity, key, value)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 200
