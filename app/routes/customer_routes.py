# import stuff
from app import db
from flask import Blueprint, jsonify, request
from app.models.customer import Customer

customer_bp = Blueprint("", __name__, url_prefix="/customers")

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
    
@customer_bp.route("", methods = ["POST"])
def post_customer():
    request_body = request.get_json()
    invalid_response = invalid_data(request_body)
    if not invalid_response:
        new_customer = Customer(
            name= request_body["name"],
            postal_code= request_body["postal_code"],
            phone= request_body["phone"] 
        )
        db.session.add(new_customer)
        db.session.commit()
        return jsonify(new_customer.to_json()), 201
    return jsonify(invalid_response), 400

@customer_bp.route("", methods = ["GET"])
def get_customers():
    customers = Customer.query.all()
    customer_list = [customer.to_json() for customer in customers]
    return jsonify(customer_list), 200

@customer_bp.route("/<customer_id>", methods = ["GET"])
def get_one_customer(customer_id):
    if customer_id.isnumeric():
        one_customer = Customer.query.get(customer_id)
        if one_customer is None:
            return jsonify({"message": f"Customer {customer_id} was not found"}), 404
        else:
            return jsonify(one_customer.to_json()), 200
    return jsonify({"message": f"Invalid customer id"}), 400
