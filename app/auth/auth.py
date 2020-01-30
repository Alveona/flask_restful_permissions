from flask_jwt_extended import (create_access_token, get_jwt_identity, jwt_required, get_raw_jwt)
from flask import Flask, request, Blueprint
from auth.models import models
from auth.handlers.register import UserRegister
from auth.handlers.login import UserLogin
from flask_restful import Api
import connection


auth_blueprint = Blueprint('auth_blueprint', __name__)
api = Api(auth_blueprint)

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')