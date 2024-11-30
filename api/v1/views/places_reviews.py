#!/usr/bin/python3
"""Route for /plase reviews
"""

from flask import jsonify, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review



@app_views.route('/places/<place_id>/reviews', methods='GET', strict_slashes=False)
def place_reviews(place_id):
    """Retrieves the list of all Place objects.
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify([review.to_dict() for review in place.reviews])

@app_views.route('/reviews/<review_id>', methods='GET', strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object.
    """
    review = storage.get("Review", review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404

    return jsonify(review.to_dict())

@app_views.route('/reviews/<review_id>', methods='DELETE', strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object.
    """
    review = storage.get("Review", review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404

    storage.delete(review)
    storage.save()

    return jsonify({}), 200

@app_views.route('/places/<place_id>/reviews', methods='POST', strict_slashes=False)
def create_review(place_id):
    """Creates a Review object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    
    user = storage.get("User", data.get("user_id"))
    if user is None:
        return jsonify({"error": "Not found"}), 404
    
    # if 'user_id' not in data:
    #     return jsonify({"error": "Missing user_id"}), 400

    if 'text' not in data:
        return jsonify({"error": "Missing text"}), 400

    review = Review(**data)
    review.place_id = place_id
    storage.new(review)
    storage.save()

    return jsonify(review.to_dict()), 201

@app_views.route('/reviews/<review_id>', methods='PUT', strict_slashes=False)
def update_review(review_id):
    """Updates a Review object.
    """
    review = storage.get("Review", review_id)
    if review is None:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key == "id" or key == "created_at" or key == "updated_at" or key == "place_id" or key == "user_id":
            continue
        setattr(review, key, value)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 200
