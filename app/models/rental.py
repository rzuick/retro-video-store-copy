from app import db
from app.models.video import Video
from app.models.customer import Customer
from datetime import datetime, timedelta

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean, default = False)

    def rental_by_title(self):
        video = Video.query.get(self.video_id)
        return{
            "title": video.title
        }

    def cust_by_name(self):
        customer = Customer.query.get(self.customer_id)
        return {
            "name": customer.name
        }

    def rental_json(self):
        pass