from flask_restplus import Api
from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from .file import api as file
from .portfolios import api as portfolios

# db = SQLAlchemy()
# flask_bcrypt = Bcrypt()

api_bluePrint = Blueprint('api', __name__)

api = Api(api_bluePrint,
          title='Realxdata API',
          version='1.0',
          description='API service'
          )

api.add_namespace(file, path='/file')
api.add_namespace(portfolios, path='/portfolios')
