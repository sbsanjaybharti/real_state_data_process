import os
from ..main import db
from api.model.fileModel import fileModel
from flask import current_app

class fileService:

    @staticmethod
    def set(file):
        file_obj = fileModel(
            name=file,
            path=os.path.join(current_app.config['UPLOAD_FOLDER'], file),
            status=0
        )
        file_obj.save()
        return file_obj


