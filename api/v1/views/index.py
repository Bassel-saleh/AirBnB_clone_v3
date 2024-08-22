#!/usr/bin/python3
"""
create FLASK app, app_views
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def api_status():
    """
    create status for app_views
    """
    response = {"status": "ok"}
    return jsonify(response)


@app_views.route('/stats')
def get_stats():
    """
    gets all stats of data
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
