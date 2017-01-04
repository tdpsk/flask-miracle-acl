'''
flask_miracle.decorators
------------------------
decorators that can be used on Flask endpoints
'''

from flask import current_app
from werkzeug.exceptions import Forbidden
from functools import wraps


class macl_check_any():
    """
    Decorator to check the currently set roles of the Acl class (see
    set_current_roles on Acl class for details) if any of them have access
    to the resource / permission combination
    """
    resource = ''
    permission = ''

    def __init__(self, resource='', permission=''):
        self.resource = resource
        self.permission = permission

    def __call__(self, func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            role = kwargs.get('macl_role', None)
            macl = current_app.miracle_acl_manager
            if not macl.check_any(self.resource, self.permission, role):
                raise Forbidden(macl.get_error_message())

            # Authenticated, run the function
            return func(*args, **kwargs)
        return func_wrapper


class macl_check_all():
    """
    Decorator to check the currently set roles of the Acl class (see
    set_current_roles on Acl class for details) if all of them have access
    to the resource / permission combination
    """
    resource = ''
    permission = ''

    def __init__(self, resource='', permission=''):
        self.resource = resource
        self.permission = permission

    def __call__(self, func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            role = kwargs.get('macl_role', None)
            macl = current_app.miracle_acl_manager
            if not macl.check_all(self.resource, self.permission, role):
                raise Forbidden(macl.get_error_message())

            # Authenticated, run the function
            return func(*args, **kwargs)
        return func_wrapper
