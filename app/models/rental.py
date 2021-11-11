from sqlalchemy.orm import backref
from app import db

class Rental(db.Model):
    __tablename__ = "rentals"
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    customer = db.relationship("Customer", backref="customers")
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    video = db.relationship("Video", backref="videos")