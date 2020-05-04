import unittest
from api.service.dataProcessService import assetData

from test.base import BaseTestCase

#############################################################################
# Class for testing service business logic
#############################################################################
class TestDataProcessService(BaseTestCase):
    def test_valid_asset(self):
        """Testing the invalid data for asset table"""

        asset = {
            'asset_ref': 'Houses',
            'portfolio': 'A_1',
            'asset_address': 'Am Kupfergraben 6',
            'asset_zipcode': '10117',
            'asset_city': 'Berlin',
            'asset_is_restricted': True,
            'asset_yoc': 1876,
            'data_timestamp': '01.01.19'
        }
        obj = assetData(asset)
        output = obj.set()
        self.assertTrue(isinstance(output, object))

