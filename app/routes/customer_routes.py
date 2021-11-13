from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.rental import Rental
from app.models.video import Video
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


def invalid_data(request_body):
    if "name" not in request_body:
        valid = {"details": "Request body must include name."}
    elif "phone" not in request_body:
        valid = {"details": "Request body must include phone."}
    elif "postal_code" not in request_body:
        valid = {"details": "Request body must include postal_code."}
    else:
        valid = False
    return valid


def invalid_customer(customer_id):
    invalid = False
    if not customer_id.isnumeric():
        invalid = {"message": f"Invalid customer id"}, 400
    elif customer_id.isnumeric():
        if Customer.query.get(customer_id) is None:
            invalid = {"message": f"Customer {customer_id} was not found"}, 404
    return invalid


@customers_bp.route("", methods=["POST"])
def post_customer():
    request_body = request.get_json()
    invalid_response = invalid_data(request_body)
    if not invalid_response:
        new_customer = Customer(
            name=request_body["name"],
            postal_code=request_body["postal_code"],
            phone=request_body["phone"]
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.to_json()), 201
    return jsonify(invalid_response), 400


@customers_bp.route("", methods=["GET"])
def get_customers():
    customers = Customer.query.all()
    customer_list = [customer.to_json() for customer in customers]
    return jsonify(customer_list), 200


@customers_bp.route("/<customer_id>", methods=["GET"])
def get_one_customer(customer_id):
    invalid_response = invalid_customer(customer_id)
    if invalid_response:
        return invalid_response
    one_customer = Customer.query.get(customer_id)
    return jsonify(one_customer.to_json()), 200

@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_cust_rental(customer_id):
    if Customer.query.get(customer_id) is None:
        return jsonify({"message": f"Customer {customer_id} was not found"}), 404
    all_rentals = Rental.query.filter_by(customer_id = customer_id) # get rental by cust_id
    response = []
    for rental in all_rentals: # to access formatted rental information
        response.append(rental.rental_by_title())
    return jsonify(response), 200


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    one_customer = Customer.query.get(customer_id)
    invalid_cust = invalid_customer(customer_id)
    if invalid_cust:
        return invalid_cust
    request_body = request.get_json()
    invalid_response = invalid_data(request_body)
    if invalid_response:
        return jsonify(invalid_response), 400
    one_customer.name = request_body["name"]
    one_customer.phone = request_body["phone"]
    one_customer.postal_code = request_body["postal_code"]
    db.session.commit()
    return jsonify(one_customer.to_json()), 200


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    one_customer = Customer.query.get(customer_id)
    invalid_cust = invalid_customer(customer_id)
    if invalid_cust:
        return invalid_cust
    db.session.delete(one_customer)
    db.session.commit()
    return jsonify(one_customer.to_json()), 200
