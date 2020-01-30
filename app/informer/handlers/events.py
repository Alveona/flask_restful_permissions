from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from informer.models.models import Event
from auth.models.models import Account, AccessGroup
from auth.decorators.access_decorators import set_public_permissions, set_private_permissions
import json


class EventsHandler(Resource):
    parser_post = reqparse.RequestParser()
    parser_post.add_argument('title', type=str, required=True, help="This field cannot be blank.")
    parser_post.add_argument('description', type=str)

    @jwt_required
    @set_public_permissions(r = True, w = True, m = False)
    def post(self):
        data = self.parser_post.parse_args()
        event = Event(title=data['title'], description=data['description'])
        event.save()
        return json.loads(event.to_json()), 201

    @jwt_required
    @set_public_permissions(r = True, w = False, m = False)
    def get(self):
        account = Account.objects.filter(user = get_jwt_identity()).first()
        event = Event.objects.protected_filter(account = account)
        return json.loads(event.to_json()), 201

class EventHandler(Resource):

    @jwt_required
    @set_private_permissions(r = True, w = False, m = False, Resource = Event, param = 'event_id', location = 'path')
    def get(self, event_id):
        event = Event.objects.filter(id = event_id).first()
        return json.loads(event.to_json()), 201

    parser_put = reqparse.RequestParser()
    parser_put.add_argument('title', type=str, required=True, help="This field cannot be blank.")
    parser_put.add_argument('description', type=str)

    @jwt_required
    @set_public_permissions(r = True, w = True, m = False)
    def put(self, event_id):
        data = self.parser_put.parse_args()
        event = Event.objects.filter(id = event_id).first()
        if not event:
            return {"message":"Event not found"}, 404

        for key, value in data.items():
            if data[key]:
                setattr(object, key, value)
        event.save()
        return json.loads(event.to_json()), 200


