from werkzeug.utils import cached_property
from flask_restplus import Api
from flask import Blueprint

from app.main.controller.ia_controller import api as ia_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API Jurimetric',
          version='1.0',
          description='a Jurimetric api with flask restplus web service'
          )

api.add_namespace(ia_ns, path='/hello')