import os
from flask import Flask, request, jsonify, current_app

from flask_sqlalchemy import SQLAlchemy
import datetime
from ..config import config_by_name
from celery import Celery
from ..service.dataProcessService import dataProcess
from ..model.fileModel import fileModel
import uuid

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend='rpc://',
        broker='amqp://rabbitmq:rabbitmq@rabbit1:5672/'
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config_by_name[os.getenv('FLASK_CONFIG') or 'development'])

db = SQLAlchemy()
db.init_app(app)

celery = make_celery(app)


@celery.task(name='celery.task.data')
def dataCreate(data):

    process = dataProcess()
    process.processStart(data)




