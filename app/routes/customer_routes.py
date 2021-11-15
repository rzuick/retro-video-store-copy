from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer
from app.models.rental import Rental
from .helper import invalid_cust_data, invalid_customer
customers_bp = Blueprint("customers", __name__, url_prefix="/customers")


@customers_bp.route("", methods=["POST"])
def post_customer():
    request_body = request.get_json()
    invalid_response = invalid_cust_data(request_body)
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
    if invalid_customer(customer_id):
        return invalid_customer(customer_id)
    one_customer = Customer.query.get(customer_id)
    return jsonify(one_customer.to_json()), 200


@customers_bp.route("/<customer_id>/rentals", methods=["GET"])
def get_cust_rental(customer_id):
    if invalid_customer(customer_id):
        return invalid_customer(customer_id)
    all_rentals = Rental.query.filter_by(
        customer_id=customer_id)  # get rental by cust_id
    response = [rental.rental_by_title() for rental in all_rentals]
    return jsonify(response), 200


@customers_bp.route("/<customer_id>", methods=["PUT"])
def update_customer(customer_id):
    one_customer = Customer.query.get(customer_id)
    if invalid_customer(customer_id):
        return invalid_customer(customer_id)
    request_body = request.get_json()
    if invalid_cust_data(request_body):
        return jsonify(invalid_cust_data(request_body)), 400
    one_customer.name = request_body["name"]
    one_customer.phone = request_body["phone"]
    one_customer.postal_code = request_body["postal_code"]
    db.session.commit()
    return jsonify(one_customer.to_json()), 200


@customers_bp.route("/<customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    one_customer = Customer.query.get(customer_id)
    if invalid_customer(customer_id):
        return invalid_customer(customer_id)
    db.session.delete(one_customer)
    db.session.commit()
    return jsonify(one_customer.to_json()), 200
