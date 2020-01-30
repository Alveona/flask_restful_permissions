# flask_restful_permissions
Template project for demonstration of using access groups with Flask_Restful and mongoengine

### Usage 

`Note:` Main authentication mechanism in this project is flask_jwt_extended with user.id as token identity  

#### Custom decorators

Permissions available:
- 'r' - read
- 'w' - write
- 'm' - manage

---------

    @jwt_required
    @set_public_permissions(r = True, w = True, m = False)
    def post(self):
      pass
        
        
Specifies resource as public one, which means decorator will only check `global_read`, `global_write` and `global_manage` permissions of account
       
---------

    @jwt_required
    @set_private_permissions(r = True, w = False, m = False, Resource = Event, param = 'event_id', location = 'path')
    def get(self, event_id):
      pass
      
Specifies private resource, the decorator will check if user's account has access groups which is listed in `group_whitelist_read` of resource


More docs are written as pydocstrings in `auth/decorators/access_decorators.py`  

---------

#### Custom QuerySet

    account = Account.objects.filter(user = get_jwt_identity()).first()
    event = Event.objects.protected_filter(account = account)
        
  `protected_filter` returns a list of resources where for each resource it is checked if user's access groups are suitable or if resource is public
