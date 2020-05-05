import json
import requests
from test.base import BaseTestCase
from api.main import db
from run import app

#############################################################################
# Class for testing service business logic
#############################################################################
class TestPortfolioUrl(BaseTestCase):
    def test_valid_asset(self):
        """ Base Tests """

        def test_valid_portfolio_list(self):
            domain = app.config['ALLOWED_HOST']
            headers = {
                'Content-type': 'application/json'
            }
            url = domain + '/portfolios'
            response_dict = json.loads(requests.get(url, headers=headers).text)

            self.assertTrue(response_dict['code'] is 200)


    def test_valid_portfolio_detail(self):
        domain = app.config['ALLOWED_HOST']
        headers = {
            'Content-type': 'application/json'
        }
        url = domain + '/portfolios'
        response_dict = json.loads(requests.get(url, headers=headers).text)

        self.assertTrue(response_dict['code'] is 200)