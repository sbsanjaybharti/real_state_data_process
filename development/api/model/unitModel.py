from ..main import db
import datetime
import uuid


class unitModel(db.Model):
    __tablename__ = 'unit'

    id = db.Column(db.String(100), primary_key=True, autoincrement=False, unique=True, default=str(uuid.uuid4()))
    ref = db.Column(db.String(100), index=True)
    asset_id = db.Column(db.String(100), db.ForeignKey('asset.id', ondelete='CASCADE'), nullable=True)
    size = db.Column(db.Integer(), index=True)
    is_rented = db.Column(db.Boolean(), index=True)
    rent = db.Column(db.Integer(), index=True)
    type = db.Column(db.String(100), default=False)
    tenant = db.Column(db.String(100), index=True)
    lease_start = db.Column(db.DateTime, nullable=True)
    lease_end = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()