import os
import unittest

from flask import current_app
from flask_testing import TestCase
from run import app

class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('api.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'mysql://{}:{}@{}/{}'.format(
                app.config['DB_USER'], app.config['DB_PASSWORD'], app.config['DB_HOST'], app.config['DB_NAME']
            )
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('api.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'my_precious')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'mysql://{}:{}@{}/{}'.format(
                app.config['DB_USER'], app.config['DB_PASSWORD'], app.config['DB_HOST'], app.config['DB_NAME']
            )
        )


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('api.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()