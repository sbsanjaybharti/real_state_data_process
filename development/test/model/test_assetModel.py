import unittest
from api.model.assetModel import assetModel, rent, area, assetModelUnit
from api.model.unitModel import unitModel

from test.base import BaseTestCase
from api.main import db
import datetime

#############################################################################
# Class for testing service business logic
#############################################################################
class TestAssetModel(BaseTestCase):
    def test_valid_asset(self):

        asset = assetModel(
            ref='A_1',
            portfolio='Houses',
            address='Am Kupfergraben 6',
            zipcode='10117',
            city='Berlin',
            is_restricted=True,
            yoc=1876,
        )
        """Testing the invalid data for asset table"""

        db.session.add(asset)
        db.session.commit()

        self.assertTrue(isinstance(asset.units, object))
        self.assertTrue(asset.ref, 'A_1')
        self.assertTrue(asset.yoc, 1876)

    def test_unit_asset(self):
        """Testing the invalid data for asset table"""

        asset = assetModel(
            ref='A_1',
            portfolio='Houses',
            address='Am Kupfergraben 6',
            zipcode='10117',
            city='Berlin',
            is_restricted=True,
            yoc=1876,
        )
        db.session.add(asset)
        db.session.commit()

        unit = unitModel(
            ref='A_1_1',
            asset_id=asset,
            size=130,
            is_rented=True,
            rent=900,
            type='RESIDENTIAL',
            tenant='xyz',
            lease_start=datetime.datetime.strptime('01.01.90','%d.%m.%y').strftime('%Y-%m-%d'),
            lease_end=datetime.datetime.strptime('01.01.90','%d.%m.%y').strftime('%Y-%m-%d'),
            created_at=datetime.datetime.strptime('01.01.90','%d.%m.%y').strftime('%Y-%m-%d'),
            updated_at=datetime.datetime.strptime('01.01.90','%d.%m.%y').strftime('%Y-%m-%d')
        )
        db.session.add(asset)
        db.session.commit()

        self.assertEqual(unit.asset_id.id, asset.id)

    def test_unit_asset(self):
        """Testing the invalid data for asset table"""

        asset = assetModel(
            ref='A_1',
            portfolio='Houses',
            address='Am Kupfergraben 6',
            zipcode='10117',
            city='Berlin',
            is_restricted=True,
            yoc=1876,
        )
        db.session.add(asset)
        db.session.commit()

        unit = unitModel(
            ref='A_1_1',
            asset_id=asset.id,
            size=130,
            is_rented=True,
            rent=900,
            type='RESIDENTIAL',
            tenant='xyz',
            lease_start=datetime.datetime.strptime('01.01.90','%d.%m.%y').strftime('%Y-%m-%d'),
            lease_end=datetime.datetime.strptime('01.01.90','%d.%m.%y').strftime('%Y-%m-%d'),
            created_at=datetime.datetime.strptime('01.01.90','%d.%m.%y').strftime('%Y-%m-%d'),
            updated_at=datetime.datetime.strptime('01.01.90','%d.%m.%y').strftime('%Y-%m-%d')
        )
        db.session.add(unit)
        db.session.commit()
        obj = rent(asset.units)

        self.assertEqual(obj.total(), 900)
        self.assertEqual(obj.fees(), [900])

