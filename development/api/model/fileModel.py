from ..main import db
import datetime


class fileModel(db.Model):
    __tablename__ = 'file'

    id = db.Column(db.Integer(), primary_key=True, index=True)
    name = db.Column(db.String(100), nullable=True)
    path = db.Column(db.String(100), nullable=True)
    status = db.Column(db.Boolean(), index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    update_at = db.Column(db.DateTime, nullable=True)
    def save(self):
        db.session.add(self)
        db.session.commit()