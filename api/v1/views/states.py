#!/usr/bin/python3
"""Route for /states
"""

from flask import jsonify, request

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects.
    """ 
    state_dicts = []
    
    sortedVal = sorted(storage.all(State).values(), key=lambda state: state.name)
    
    # for state in sortedVal:
    #     state_dict = state.to_dict()
    #     state_dicts.append(state_dict)
    
    # OR by Using List Comprehension
    state_dicts = [state.to_dict() for state in sortedVal]
    return jsonify(state_dicts)

    # with out sorting
    # states = storage.all(State)
    # return jsonify([state.to_dict() for state in states.values()])

@app_views.route('/states/<id>', methods=['GET'], strict_slashes=False)
def get_states_by_id(id):
    """Retrieves the list of all State objects.
    """
    val  = storage.get(State, id)
    if val is None:
        return jsonify({"error": "Not found"}), 404
    
    # Convert the state to a dictionary and return it
    state = val.to_dict()
    return jsonify(state)

@app_views.route('/states/<id>', methods=['DELETE'], strict_slashes=False)
def delete_state(id):
    """Deletes a State object.
    """
    if not id:
        return jsonify({"error": "To Delete State ID is required"}), 400
    
    state = storage.get(State, id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    
    storage.delete(state)
    storage.save()
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Method to create a new state.
    """
    data = request.get_json()
    
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<id>', methods=['PUT'], strict_slashes=False)
def update_state(id):
    """ Method to update a state.
    """
    state = storage.get(State, id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    
    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    
    for key, value in data.items():
        if key == 'id' or key == 'created_at' or key == 'updated_at':
            continue
        setattr(state, key, value)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 200
