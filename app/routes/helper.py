from flask import request
from app.models.video import Video
from app.models.rental import Rental
from app.models.customer import Customer

def invalid_cust_data(request_body):
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

def invalid_video_data(request_body):
    if "title" not in request_body:
        valid = {"details": "Request body must include title."}
    elif "release_date" not in request_body:
        valid = {"details": "Request body must include release_date."}
    elif "total_inventory" not in request_body:
        valid = {"details": "Request body must include total_inventory."}
    else:
        valid = False
    return valid

def invalid_video(video_id):
    invalid = False
    if not video_id.isnumeric():
        invalid = {"message": f"Invalid video id"}, 400
    elif video_id.isnumeric():
        if Video.query.get(video_id) is None:
            invalid = {"message": f"Video {video_id} was not found"}, 404
    return invalid

def invalid_rental_data(request_body):
    if "customer_id" not in request_body:
        invalid = {"details": "Request body must include customer_id."}
    elif "video_id" not in request_body:
        invalid = {"details": "Request body must include video_id."}
    else:
        invalid = False
    return invalid
