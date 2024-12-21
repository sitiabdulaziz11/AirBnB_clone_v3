#!/usr/bin/python3
"""Route for /places
"""

from flask import jsonify, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.state import State


@app_views.route('/cities/city_id/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects.
    """
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404
    
    places = storage.all(Place).values()
    if places is None:
        return jsonify({"error": "Not found"}), 404
    
    return jsonify([place.to_dict() for place in places.values()])

@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """Retrieves a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a Place object.
    """
    city = storage.get(City, city_id)
    if city is None:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    if data.get("user_id") is None:
        return jsonify({"error": "Missing user_id"}), 400

    if data.get("name") is None:
        return jsonify({"error": "Missing name"}), 400

    new_place = Place(**data)
    new_place.city_id = city.id
    # new_place.city_id = city_id   #  City object corresponding to the city_id, but this does validate the city_id implicitly.
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key == "id" or key == "created_at" or key == "updated_at" or key == "city_id" or key == "user_id":
            continue
        setattr(place, key, value)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 200

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def place_search():
    """Search or retrieve place object based on specific filters passed in the JSON body of the request.
    """
    try:
        data = request.get_json()
    except Exception:
        return jsonify({"error": "Not a JSON"}), 400
    
    if not data or not any(data.values()):
        places = storage.all(Place).value()
        return jsonify([place.to_dict() for place in places])
    
    # Retrieve filters
    states = data.get("states", [])
    cities = data.get("cities", [])
    amenities = data.get("amenities", [])
    
    # Get Place objects
    places = []
    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    places.extend(city.places)  #  Instead of appending one Place
                    # object at a time with append(), extend() can add all Place objects in one step.
    
    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                   places.extend(city.places)
    
    # Remove duplicates
    # places = list(set(places))
    
    # Filter by amenities
    if amenities:
        places = [place for place in places if all(amenity.id in [a.id for a in place.amenities] for amenity in amenities)]
    return jsonify([place.to_dict() for place in places])
