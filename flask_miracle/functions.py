'''
flask_miracle.functions
-----------------------
functions callable from within a Flask context
'''

from flask import current_app


def check_any(resource, permission, roles=None):
    return current_app.miracle_acl_manager.check_any(resource, permission, roles=None)

def check_all(resource, permission, roles=None):
    return current_app.miracle_acl_manager.check_all(resource, permission, roles=None)

def set_current_roles(roles):
    return current_app.miracle_acl_manager.set_current_roles(roles)
