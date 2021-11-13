from app import db
from flask import Blueprint, jsonify, request
from app.models.rental import Rental
from app.models.customer import Customer
from app.models.video import Video
from datetime import timedelta, datetime

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
    video_current_checked_out = Rental.query.filter_by(checked_out=True, video_id=one_video.id).count()
    available_inventory = one_video.total_inventory - video_current_checked_out
    if available_inventory == 0:
        return jsonify({"message": "Could not perform checkout"}), 400
    new_rental = Rental(
        customer_id=one_customer.id,
        video_id = one_video.id,
        due_date = (datetime.now(tz=None) + timedelta(days=7)),
        checked_out = True
    )
    db.session.add(new_rental)
    db.session.commit()
    cust_current_checked_out = Rental.query.filter_by(customer_id=one_customer.id, checked_out=True).count()
    available_inventory -=1
    response_body = {
        "customer_id": one_customer.id,
            "video_id": one_video.id,
            "due_date": new_rental.due_date,
            "videos_checked_out_count": cust_current_checked_out,
            "available_inventory": available_inventory
    }
    return jsonify(response_body), 200

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
    video_current_checked_in = Rental.query.filter_by(checked_out=True).count()
    video_checked_out = Rental.query.filter_by(checked_out=False).count()
    if video_current_checked_in == 0:
        return jsonify({"message": f"No outstanding rentals for customer {one_customer.id} and video {one_video.id}"}), 400
    returned_rental = Rental(
        customer_id = one_customer.id,
        video_id = one_video.id,
        checked_out = False
    )
    db.session.add(returned_rental)
    db.session.commit()
    available_inventory = one_video.total_inventory - video_checked_out
    response_body = {
        "customer_id": one_customer.id,
        "video_id": one_video.id,
        "videos_checked_out_count": video_checked_out,
        "available_inventory": available_inventory
            }
    return jsonify(response_body), 200

