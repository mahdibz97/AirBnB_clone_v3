#!/usr/bin/python3
""" Handling  Api for states"""


from models.state import State
from models import storage
from api.v1.views import app_views
from flask import jsonify, make_response, abort, request


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    '''get all states'''
    obj = []
    states = storage.all("State").values()
    for i in states:
        obj.append(i.to_dict())
    return jsonify(obj)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state_byid(state_id):
    """get state by id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_byid(state_id):
    """ delete state by id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def creat_new_state():
    """creat new state"""
    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'name' not in request.get_json().keys():
        abort(400, description='Missing name')

    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update state"""
    state = storage.get("State", state_id)

    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    state.name = data['name']
    state.save()
    return jsonify(state.to_dict())
