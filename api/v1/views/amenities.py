#!/usr/bin/python3
"""
Handles all RESTful API actions for `Amenity`
"""
from api.v1.views import app_views
from models import storage
from models import amenity
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route("/amenities", strict_slashes=False)
def get_all_amenities():
    """Retrieve list of all Amenities"""
    amenity_list = []
    for key, value in storage.all(Amenity).items():
        amenity_list.append(value.to_dict())
    return jsonify(amenity_list)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieve one `Amenity`

    Args:
        amenity_id (str): Amenity identifier

    Returns:
        flask.Response: An amenity in json
    """
    target = storage.get(Amenity, amenity_id)
    if target:
        return jsonify(target.to_dict())
    else:
        return abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Delete amenity

    Args:
        amenity_id (str): The ID of the amenity.

    Returns:
        dict: An empty JSON.

    Raises:
        404: If the specified amenity_id does not exist.
    """
    target = storage.get(Amenity, amenity_id)
    if target:
        storage.delete(target)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def create_amenity():
    """Create an amenity

    Returns:
        dict: New amenity in JSON

    Raises:
        400: If request body is not a valid JSON
        400: If the payload does not contain the key `name`
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()

    if 'name' not in data:
        return abort(400, 'Missing name')

    target = Amenity(**data)

    target.save()

    return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    updates amenity
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()

    target = storage.get(Amenity, amenity_id)
    if target:
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(target, key, value)
        target.save()
        return jsonify(target.to_dict()), 200
    else:
        return abort(404)
