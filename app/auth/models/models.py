import mongoengine_goodjson as gj
from mongoengine import *

class User(gj.Document):
    meta = {
        'collection': 'users'
    }
    username = StringField(max_length=120, required=True, unique=True)
    hashpw = StringField(max_length=255, required=True, exclude_to_json=True)

class Account(gj.Document):
    meta = {
        'collection': 'accounts'
    }

    name = StringField(max_length=120, required=True)
    user = ReferenceField(User, reverse_delete_rule=CASCADE, exclude_to_json=True)
    access_groups = ListField(ReferenceField('AccessGroup'), exclude_to_json=True)
    deleted = BooleanField(default = False, exclude_to_json=True)

class AccessGroup(gj.Document):
    meta = {
        'collection': 'access_groups'
    }

    title = StringField(max_length=120, required=True)
    users = ListField(ReferenceField(Account))
    pre_defined = BooleanField(default=False)
    global_read = BooleanField(default=True)
    global_write = BooleanField(default=False)
    global_manage = BooleanField(default=False)
