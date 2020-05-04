import os
from flask import Flask, current_app
from werkzeug.utils import secure_filename

class fileFilter:

    def __init__(self, file):
        self.file = file
        self.filename = file.filename
        self.ALLOWED_EXTENSIONS = {'csv'}

    def allowed_file(self):
        if '.' in self.filename and self.filename.rsplit('.', 1)[1].lower() in self.ALLOWED_EXTENSIONS:
            return self.file
        else:
            return False

class files:
    def __init__(self, file):
        self.file = fileFilter(file).allowed_file()

    def upload(self):
        if self.file:
            self.file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], secure_filename(self.file.filename)))
            response_object = {
                'code': 200,
                'type': 'Success',
                'message': 'File uploaded'
                }
            return response_object
        else:
            response_object = {
                'code': 400,
                'type': 'Error',
                'message': 'Invalid file type'
                }
            return response_object
