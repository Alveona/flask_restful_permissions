from flask_restful import Resource, reqparse
from auth.models.models import User, Account, AccessGroup
import bcrypt
import json

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('username', type=str, required=True, help="This field cannot be blank.")
    parser.add_argument('password', type=str, required=True, help="This field cannot be blank.")

    def post(self):
        data = self.parser.parse_args()
        username = data['username']
        password = data['password']
        hashpw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        user = User(username = username, hashpw = hashpw)
        user.save()
        name = data['name']
        account = Account(name = name, user = user)
        guest_group = AccessGroup.objects.filter(pre_defined = True, title = 'Посетитель').first()
        account.access_groups.append(guest_group)
        account.save()
        return json.loads(account.to_json())