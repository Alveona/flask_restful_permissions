import mongoengine_goodjson as gj
from mongoengine import *
from auth.models.models import AccessGroup
from mongoengine.queryset.visitor import Q


class BaseCustomQuerySet(gj.QuerySet):

    def protected_filter(self, account, *args, **kwargs):
        objects = self.filter(Q(group_whitelist_read__in = account.access_groups, *args, **kwargs) | Q(private = False, *args, **kwargs))
        return objects

class Event(gj.Document):
    meta = {
        'collection': 'events',
        'queryset_class': BaseCustomQuerySet
    }

    title = StringField(max_length=120, required=True)
    description = StringField(max_length=255, required=False)
    private = BooleanField(default=False)
    group_whitelist_read = ListField(ReferenceField(AccessGroup))
