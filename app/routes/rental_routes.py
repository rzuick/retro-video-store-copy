from app import db
from flask import Blueprint, jsonify, request
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from datetime import datetime, timedelta

rentals_bp = Blueprint("rentals", __name__, url_prefix="/rentals")

def invalid_data(request_body):
    if "customer_id" not in request_body:
        invalid = {"details": "Request body must include customer_id."}
    elif "video_id" not in request_body:
        invalid = {"details": "Request body must include video_id."}
    else:
        invalid = False
    return invalid

@rentals_bp.route("/check-out", methods=["POST"])
def post_rental():
    request_body = request.get_json()
    invalid_request = invalid_data(request_body)
    if invalid_request:
        return jsonify(invalid_request), 400

    one_video = Video.query.get(request_body["video_id"])
    one_customer = Customer.query.get(request_body["customer_id"])
    if one_video is None:
        return jsonify({"Bad Request": f"Video not found."}), 404
    elif one_customer is None:
        return jsonify({"Bad Request": f"Customer not found."}), 404

    new_rental = Rental(
        customer_id=one_customer.id,
        video_id = one_video.id
    )
    db.session.add(new_rental)
    db.session.commit()
    all_rentals = Rental.query.all()
    if len(all_rentals) > one_video.total_inventory:
        return jsonify({"message": "Could not perform checkout"}), 400
    return jsonify(new_rental.to_json()), 200

@rentals_bp.route("/check-in", methods=["POST"])
def post_rental_return():
    request_body = request.get_json()
    invalid_request = invalid_data(request_body)
    if invalid_request:
        return jsonify(invalid_request), 400
    
    one_video = Video.query.get(request_body["video_id"])
    one_customer = Customer.query.get(request_body["customer_id"])
    if one_video is None:
        return jsonify({"Bad Request": f"Video not found."}), 404
    elif one_customer is None:
        return jsonify({"Bad Request": f"Customer not found."}), 404
    returned_rental = Rental(
        customer_id = one_customer.id,
        video_id = one_video.id
    )
    db.session.add(returned_rental)
    db.session.commit()
    all_rentals = Rental.query.all()
    if len(all_rentals) == one_video.total_inventory:
        return jsonify({"message": f"No outstanding rentals for customer {one_customer.id} and video {one_video.id}"}), 400
    return jsonify(returned_rental.to_json_returned()), 200
