from app import db
from flask import Blueprint, jsonify, request
from app.models.video import Video
from app.models.rental import Rental
from .helper import invalid_video, invalid_video_data

video_bp = Blueprint("video_bp", __name__, url_prefix="/videos")


@video_bp.route("", methods=["GET"])
def get_videos():
    videos = Video.query.all()
    video_list = [video.video_dict() for video in videos]
    return jsonify(video_list), 200


@video_bp.route("/<video_id>", methods=["GET"])
def get_one_video(video_id):
    if invalid_video(video_id):
        return invalid_video(video_id)
    one_video = Video.query.get(video_id)
    return jsonify(one_video.video_dict()), 200


@video_bp.route("/<video_id>/rentals", methods=["GET"])
def get_vid_rental(video_id):
    if invalid_video(video_id):
        return jsonify(invalid_video(video_id)), 404
    all_videos = Rental.query.filter_by(
        video_id=video_id)  # get rental by cust_id
    response = [video.cust_by_name() for video in all_videos]
    return jsonify(response), 200


@video_bp.route("", methods=["POST"])
def post_video():
    request_body = request.get_json()
    if not invalid_video_data(request_body):
        new_video = Video(
            title=request_body["title"],
            release_date=request_body["release_date"],
            total_inventory=request_body["total_inventory"]
        )
        db.session.add(new_video)
        db.session.commit()
        return jsonify(new_video.video_dict()), 201
    return jsonify(invalid_video_data(request_body)), 400


@video_bp.route("/<video_id>", methods=["PUT"])
def update_video(video_id):
    one_video = Video.query.get(video_id)
    if invalid_video(video_id):
        return invalid_video(video_id)
    request_body = request.get_json()
    if invalid_video_data(request_body):
        return jsonify(invalid_video_data(request_body)), 400
    one_video.title = request_body["title"]
    one_video.release_date = request_body["release_date"]
    one_video.total_inventory = request_body["total_inventory"]
    db.session.commit()
    return jsonify(one_video.video_dict()), 200


@video_bp.route("/<video_id>", methods=["DELETE"])
def delete_video(video_id):
    one_video = Video.query.get(video_id)
    if invalid_video(video_id):
        return invalid_video(video_id)
    db.session.delete(one_video)
    db.session.commit()
    return jsonify(one_video.video_dict()), 200
