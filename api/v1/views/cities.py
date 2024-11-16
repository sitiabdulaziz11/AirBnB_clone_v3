#!/usr/bin/python3
"""Route for /cities
"""

from flask import jsonify, request

from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City



@app_views.route('/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects withn a state.
    """
    state = storage.get(State, state_id)
    # cities = storage.all(City).values()
    
    if state is None:
        return jsonify({"error": "Not found"}), 404
    
    city_dict = []
    
    for city in state.cities:
        city_dict.append(city.to_dict())
    return jsonify(city_dict)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """ Retrieves a specific City object.
    """
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City object.
    """
    if not city_id:
        return jsonify({"error": "To Delete City ID is required"}), 400
    
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Method to create a new city.
    """
    data = request.get_json()
    
    state = storage.get(State, state_id)
    # print(state)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    
    city = City(**data)
    city.state_id = state.id  # Explicitly set the state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Method to update a city.
    """
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at' or key == 'state_id':
            continue
        setattr(city, key, value)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 200
