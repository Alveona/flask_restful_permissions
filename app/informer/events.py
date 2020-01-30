from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required, get_raw_jwt)
from flask import Flask, request, Blueprint
from auth.models import models
from informer.handlers.events import EventHandler, EventsHandler
from flask_restful import Api
import connection


events_blueprint = Blueprint('events_blueprint', __name__)
api = Api(events_blueprint)

api.add_resource(EventsHandler, '/events')
api.add_resource(EventHandler, '/event/<event_id>')