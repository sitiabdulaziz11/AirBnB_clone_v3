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
    val  = storage.all(State)
    for state in val:
        res = state.to_dict()
    return jsonify(res)

    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])

@app_views.route('/states<id>', methods=['GET'], strict_slashes=False)
def get_states_by_id(id):
    """Retrieves the list of all State objects.
    """ 
    val  = storage.get(State, id)
    return jsonify(val)
