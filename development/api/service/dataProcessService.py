import os
from ..main import db
from flask import current_app
from api.model.assetModel import assetModel
from api.model.unitModel import unitModel
from ..model.fileModel import fileModel
import datetime
import uuid
import pandas as pd

#############################################################################
# Class declare in single responsible & Factory method design pattern
#############################################################################
class assetData:

    def __init__(self, asset):
        self.asset = asset
        self.ref = asset['asset_ref']

    def set(self):
        asset = assetModel(
            id=str(uuid.uuid4()),
            ref=self.asset['asset_ref'],
            portfolio=self.asset['portfolio'],
            address=self.asset['asset_address'],
            zipcode=self.asset['asset_zipcode'],
            city=self.asset['asset_city'],
            is_restricted=self.asset['asset_is_restricted'],
            yoc=self.asset['asset_yoc'],
            updated_at=datetime.datetime.strptime(self.asset['data_timestamp'],'%d.%m.%y').strftime('%Y-%m-%d') if self.asset['data_timestamp'] != '' else None,
        )
        asset.save()
        return asset

    def get(self):
        return assetModel.query.filter_by(ref=self.ref).first()

    def update(self):
        asset = assetModel.query.filter_by(ref=self.ref).first()
        # asset.address = ''
        # asset.zipcode = ''
        # asset.city = ''
        if asset.is_restricted != self.asset['asset_is_restricted']:
            asset.is_restricted = self.asset['asset_is_restricted']
        if self.asset['data_timestamp'] != '':
            asset.updated_at = datetime.datetime.strptime(self.asset['data_timestamp'],'%d.%m.%y').strftime('%Y-%m-%d')
        db.session.commit()
        return asset

    def process(self):
        current_asset = self.get()
        if current_asset:
            return self.update()
        else:
            return self.set()

class unitData:

    def __init__(self, asset, unit):
        self.asset = asset.process()
        self.unit = unit
        self.unit_ref = unit['unit_ref']
        self.unit_type = unit['unit_type']

    def set(self):
        unit = unitModel(
            id=str(uuid.uuid4()),
            ref=self.unit['unit_ref'],
            asset_id=self.asset.id,
            size=self.unit['unit_size'],
            is_rented=self.unit['unit_is_rented'],
            rent=self.unit['unit_rent'],
            type=self.unit['unit_type'],
            tenant=self.unit['unit_tenant'],
            lease_start=datetime.datetime.strptime(self.unit['unit_lease_start'],'%d.%m.%y').strftime('%Y-%m-%d') if self.unit['unit_lease_start'] != '' else None,
            lease_end=datetime.datetime.strptime(self.unit['unit_lease_end'],'%d.%m.%y').strftime('%Y-%m-%d') if self.unit['unit_lease_end'] != '' else None,
            updated_at=datetime.datetime.strptime(self.unit['data_timestamp'],'%d.%m.%y').strftime('%Y-%m-%d') if self.unit['data_timestamp'] != '' else None,
        )
        unit.save()

    def get(self):
        return unitModel.query.filter_by(ref=self.unit_ref).filter_by(type=self.unit_type).first()

    def update(self):
        unit = self.get()
        unit.size = self.unit['unit_size']
        unit.is_rented = self.unit['unit_is_rented']
        unit.rent = self.unit['unit_rent']
        unit.type = self.unit['unit_type']
        unit.tenant = self.unit['unit_tenant']
        unit.lease_start = datetime.datetime.strptime(self.unit['unit_lease_start'],'%d.%m.%y').strftime('%Y-%m-%d') if self.unit['unit_lease_start'] != '' else None,
        unit.lease_end = datetime.datetime.strptime(self.unit['unit_lease_end'],'%d.%m.%y').strftime('%Y-%m-%d') if self.unit['unit_lease_end'] != '' else None,
        unit.updated_at = datetime.datetime.strptime(self.unit['data_timestamp'],'%d.%m.%y').strftime('%Y-%m-%d') if self.unit['data_timestamp'] != '' else None
        db.session.commit()
        return unit

    # @staticmethod
    def process(self):
        current_unit = self.get()
        if current_unit:
            return self.update()
        else:
            return self.set()

class dataProcess:

    def insert(self, asset, unit):

        unitData(assetData(asset), unit).process()

        return 'Data created successfully!'
    def processStart(self, file):

        # Panda for cleaning and managing
        header_list = ["portfolio", "asset_ref", "asset_address", "asset_zipcode", "asset_city",\
                       "asset_is_restricted", "asset_yoc", "unit_ref", "unit_size", "unit_is_rented", \
                       "unit_rent", "unit_type", "unit_tenant", "unit_lease_start", "unit_lease_end", "data_timestamp"]
        df = pd.read_csv(os.path.join(current_app.config['UPLOAD_FOLDER'], file['name']), names=header_list,
                         sep=';', header=0)
        df['unit_rent'] = df['unit_rent'].fillna(0)
        df = df.fillna('')

        for row in df.to_dict(orient='records'):
            asset = {
                'asset_ref': row['asset_ref'],
                'portfolio': row['portfolio'],
                'asset_address': row['asset_address'],
                'asset_zipcode': row['asset_zipcode'],
                'asset_city': row['asset_city'],
                'asset_is_restricted': row['asset_is_restricted'],
                'asset_yoc': row['asset_yoc'],
                'data_timestamp': row['data_timestamp']
            }
            unit = {
                'unit_ref': row['unit_ref'],
                'unit_size': row['unit_size'],
                'unit_is_rented': row['unit_is_rented'],
                'unit_rent': row['unit_rent'],
                'unit_type': row['unit_type'],
                'unit_tenant': row['unit_tenant'],
                'unit_lease_start': row['unit_lease_start'],
                'unit_lease_end': row['unit_lease_end'],
                'data_timestamp': row['data_timestamp']
            }
            self.insert(asset, unit)

        file = fileModel.query.filter_by(id=file['id']).first()
        file.status = 1
        db.session.commit()