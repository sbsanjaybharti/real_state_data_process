from ..main import db
import datetime
from dateutil import relativedelta
from sqlalchemy.ext.hybrid import hybrid_property
import uuid


class assetModel(db.Model):
    __tablename__ = 'asset'

    id = db.Column(db.String(100), primary_key=True, autoincrement=False, unique=True, default=str(uuid.uuid4()))
    ref = db.Column(db.String(100), index=True)
    portfolio = db.Column(db.String(100), index=True)
    address = db.Column(db.String(100), index=True)
    zipcode = db.Column(db.Integer(), index=True)
    city = db.Column(db.String(100), index=True)
    is_restricted = db.Column(db.Boolean, default=False)
    yoc = db.Column(db.Integer(), index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    units = db.relationship('unitModel', backref='asset', lazy=True)

    def save(self):
        db.session.add(self)
        db.session.commit()

class rent:
    def __init__(self, units):
        self.units = units

    def total(self):
        return sum(unit.rent for unit in self.units)

    def fees(self):
        return [unit.rent for unit in self.units]

    def average(self):
        return round(self.total()/len(self.units))

class area:
    def __init__(self, units):
        self.units = units

    def total(self):
        return sum(unit.size for unit in self.units)

    def rented(self):
        return sum(unit.size for unit in self.units if unit.is_rented != 0)

    def rentedPercent(self):
        return "{:.2f}".format(self.rented()*100/self.total())

    def nonRentedPercent(self):
        return "{:.2f}".format(((self.total() - self.rented())*100)/self.total())

    def average(self):
        return round(self.total()/len(self.units))

    def walt(self):
        total_area = self.total()
        result = 0
        for unit in self.units:
            tanent_area = (unit.size)/total_area * relativedelta.relativedelta(unit.lease_end, datetime.datetime.now()).years
            result += tanent_area

        return "{:.2f}".format(result)

class assetModelUnit:
    def __init__(self, model):
        self.model = model
        self.rent = rent(self.model.units)
        self.area = area(self.model.units)

    def units(self):
        return len(self.model.units)
