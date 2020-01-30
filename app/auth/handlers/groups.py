from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from auth.models.models import Account, AccessGroup
import json


class GroupCreateHandler(Resource):
    parser_post = reqparse.RequestParser()
    parser_post.add_argument('title', type=str, required=True, help="This field cannot be blank.")

    @jwt_required
    def post(self):
        data = self.parser_post.parse_args()
        group = AccessGroup(title=data['title'])
        group.save()
        return json.loads(group.to_json()), 201


