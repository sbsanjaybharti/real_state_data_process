from flask_testing import TestCase
from api.main import db
from run import app

#############################################################################
# Class for basic setup for testing which can be use as a base class
#############################################################################
class BaseTestCase(TestCase):
    """ Base Tests """
    def create_app(self):
        app.config.from_object('api.config.TestingConfig')
        return app

    def setUp(self):
        db.create_all()
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

