#!/usr/bin/python3
"""Route for /states
"""

from flask import jsonify

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
    state = storage.get(State, id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    
    storage.delete(state)
    storage.save()
    return jsonify({}), 200
