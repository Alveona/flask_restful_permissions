from functools import wraps
from auth.models.models import Account
from flask_jwt_extended import get_jwt_identity
from flask import request, abort
from mongoengine import Document
import json

def set_public_permissions(r:bool = False, w:bool = False, m:bool = False):
    """
    Sets specific permissions for accessing resource  
    Resource is public, therefore decorator checks if user access group has global 'read', 'write' or 'manage' permission  

        :param r:bool=False: if user needs at least 'read' permissions to access resource
        :param w:bool=False: if user needs at least 'write' permissions to access resource
        :param m:bool=False: if user needs at least 'manage' permissions to access resource
    """
    def wrapper(f):
        @wraps(f)
        def decorated(*a, **kw):

            user = Account.objects.filter(user = get_jwt_identity()).first()
            if not user:
                abort(401, 'No credentials provided')
            
            if m == True:
                suitable_groups = [group for group in user.access_groups if group.global_manage == True]
                if not suitable_groups:
                    abort(401, 'Access denied')

            if w == True:
                suitable_groups = [group for group in user.access_groups 
                                    if group.global_manage == True
                                    or group.global_write == True]
                if not suitable_groups:
                    abort(401, 'Access denied')

            if r == True:
                suitable_groups = [group for group in user.access_groups 
                                    if group.global_manage == True
                                    or group.global_write == True
                                    or group.global_read == True]
                if not suitable_groups:
                    abort(401, 'Access denied')

            return f(*a, **kw)
        return decorated
    return wrapper


def set_private_permissions(r:bool = False, w:bool = False, m:bool = False, Resource:Document = None, param:str = None, location:str = None):
    """
    Sets specific permissions for accessing resource  
    If instance is not specified, it means that resource is public, therefore
    decorator checks if user access group has global 'read', 'write' or 'manage' permission  
    Otherwise, doesn't check global permissions, but checks only permissions for specific resource  

        :param r:bool=False: if user needs at least 'read' permissions to access resource
        :param w:bool=False: if user needs at least 'write' permissions to access resource
        :param m:bool=False: if user needs at least 'manage' permissions to access resource
        :param Resource:Document=None: resource class to check 'id' in it's collection
        :param param:str=None: name of 'param' where to find 'id' of resource
        :param location:str=None: where to find param; possible are: ['args', 'form', 'json', 'path']
    """
    def wrapper(f):
        @wraps(f)
        def decorated(*a, **kw):

            data = None
            resource_identity = None
            if location == 'args':
                data = request.args
            elif location == 'form':
                data = request.form
            elif location == 'json':
                data = request.json
            elif location == 'path':
                data = kw
            else:
                abort(400, "Can't find specified resource location")
            
            if not param in data:
                abort(400, "Can't find resource parameter")

            resource_identity = data[param]
            resource = Resource.objects.filter(id = resource_identity).first()
    
            print(resource.title)

            # user = Account.objects.filter(user = get_jwt_identity()).first()
            # if not user:
            #     abort(401, 'No credentials provided')
            
            # if m == True:
            #     suitable_groups = [group for group in user.access_groups if group.global_manage == True]
            #     if not suitable_groups:
            #         abort(401, 'Access denied')

            # if w == True:
            #     suitable_groups = [group for group in user.access_groups 
            #                         if group.global_manage == True
            #                         or group.global_write == True]
            #     if not suitable_groups:
            #         abort(401, 'Access denied')

            # if r == True:
            #     suitable_groups = [group for group in user.access_groups 
            #                         if group.global_manage == True
            #                         or group.global_write == True
            #                         or group.global_read == True]
            #     if not suitable_groups:
            #         abort(401, 'Access denied')

            return f(*a, **kw)
        return decorated
    return wrapper
