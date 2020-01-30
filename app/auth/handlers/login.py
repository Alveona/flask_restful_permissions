from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource, reqparse
from auth.models.models import User
import bcrypt
import datetime

class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True)

    def post(self):
        data = self.parser.parse_args()
        user = User.objects.filter(username=data['username']).first()
        if not user:
            return {"message": "User not found"}, 404

        password = data['password']
        if user and bcrypt.checkpw(password.encode('utf8'), user.hashpw.encode('utf8')):
            token = create_access_token(identity=str(user.id), fresh=True, expires_delta=False)
            refresh = create_refresh_token(identity=str(user.id), expires_delta=False)
            return {
                'access_token': token,
                'refresh_token': refresh
            }, 200

        return {"message": "Invalid Credentials"}, 401