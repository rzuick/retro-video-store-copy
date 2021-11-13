from sqlalchemy.orm import backref
from app import db
from app.models.video import Video
from datetime import datetime, timedelta

class Rental(db.Model):
    __tablename__ = "rentals"
    id = db.Column(db.Integer, primary_key=True, autoincrement = True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), primary_key=True, nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), primary_key=True, nullable=False)
    due_date = db.Column(db.DateTime)
    checked_out = db.Column(db.Boolean, default = False)
    videos_checked_out = db.Column(db.Integer, default=0)
    available_inventory = db.Column(db.Integer)

    def to_json(self):
        video = Video.query.get(self.video_id)
        current_day = datetime.now(tz=None)
        checkout = timedelta(days=7)
        due = current_day + checkout
        self.checked_out = True
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "due_date": due,
            "videos_checked_out_count": self.videos_checked_out +1,
            "available_inventory": video.total_inventory - 1
            }

    def to_json_returned(self):
        video = Video.query.get(self.video_id)
        self.checked_out = False
        return {
            "customer_id": self.customer_id,
            "video_id": self.video_id,
            "videos_checked_out_count": self.videos_checked_out,
            "available_inventory": video.total_inventory
            }
    def rental_by_title(self):
        video = Video.query.get(self.video_id)
        return{
            "title": video.title
        }
