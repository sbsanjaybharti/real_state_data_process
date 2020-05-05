import os
from flask import request,  jsonify, current_app
from flask_restplus import Resource, Namespace, reqparse
import werkzeug
from .utility.file import files
from api.service.fileService import fileService
from .utility.celery import dataCreate

api = Namespace('Files', description='file uploading')

# Set parameter for file upload
file_upload = reqparse.RequestParser()
file_upload.add_argument('file',
                         type=werkzeug.datastructures.FileStorage,
                         location='files',
                         required=True,
                         help='CSV file only')

@api.route('/')
class file(Resource):
    @api.expect(file_upload)
    def post(self):
        """
         API for uploading CSV data file
         ## Implementation Notes
         __Note__ : No limit for file size, Data
         1. Data cleaning will te taken care by Panda library
         2. Data transfer to database will be done by rabbitMQ with celery to reduce load and user waiting time.

        """
        args = file_upload.parse_args()
        file_obj = files(args['file'])

        response = file_obj.upload()
        file = fileService.set(args['file'].filename)

        try:
            # ********************************************
            # Celery call for process the file
            # ********************************************
            dataCreate.delay({'id': file.id, 'name': file.name})
            # ********************************************
            # Celery call for process the file
            # ********************************************
        except Exception as e:
            response_object = {
                'code': 500,
                'type': 'Internal Server Errors',
                'message': 'Exception occur in task service, Try again later!',
            }
            return response_object

        return response
