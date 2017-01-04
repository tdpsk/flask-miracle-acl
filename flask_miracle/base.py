'''
flask_miracle.base
------------------
base class for flask_miracle
'''

from miracle.acl import Acl as MiracleAcl
from flask import Flask, current_app


class Acl():
    """
    Base class that communications between Miracle ACL and Flask
    """

    acl = MiracleAcl()
    app = None

    _current_roles = []
    _roles_callback = None

    def __init__(self, app=None, acl=None):
        """
        Initialize the class and load the Flask app as well as the Miracle ACL

        Keyword arguments:
        app -- Flask app instance (default: None)
        acl -- Miracle ACL instance (default: None)
        """
        self.app = app
        self.acl = acl or MiracleAcl()

        if app is not None:
            self.init_app()

    def init_app(self):
        """
        Initialize the Flask app after it has been set
        """
        self.app.config.setdefault('MACL_DEFINITION', None)
        self.app.config.setdefault('MACL_CLASS', None)
        self.app.config.setdefault('MACL_ERROR_MESSAGE', 'You do not have access to this resource')

        self.app.miracle_acl_manager = self

        self.load_acl()

    def load_acl(self):
        """
        Load the ACL definitions from flask configuration.

        Three Flask configuration options are available:
        MACL_CLASS -- A class which defines the ACL parameters via fields
          ROLES, STRUCT and GRANTS
        MACL_DEFINITION -- A dictionary type definition of the ACL parameters
          with fields roles, structs and grants
        MACL_DEFAULT_ROLES -- The default roles as a list which are applied if
          no specific roles are given
        """
        macl_class = self.app.config.get('MACL_CLASS', None)
        macl_dict = self.app.config.get('MACL_DEFINITION', None)
        default_roles = self.app.config.get('MACL_DEFAULT_ROLES', None)

        if default_roles is not None:
            self._current_roles = default_roles

        if macl_class is not None:
            self.load_from_class(macl_class)

        if macl_dict is not None:
            self.load_from_dict(macl_dict)

    def load_from_class(self, cls):
        """
        Load acl data from class, see load_acl for details

        Arguments:
        cls -- the class to import
        """
        acl_dict = {
            'roles': [],
            'struct': {},
            'grants': {}
        }

        if hasattr(cls, 'ROLES'):
            acl_dict['roles'] = cls.ROLES

        if hasattr(cls, 'STRUCT'):
            acl_dict['struct'] = cls.STRUCT

        if hasattr(cls, 'GRANTS'):
            acl_dict['grants'] = cls.GRANTS

        return self.load_from_dict(acl_dict)

    def load_from_dict(self, acl_dict):
        """
        Load acl data from dict, see load_acl for details

        Arguments:
        acl_dict -- the dictionary to import
        """
        roles = acl_dict.get('roles', [])
        struct = acl_dict.get('struct', {})
        grants = acl_dict.get('grants', {})

        self.acl.add_roles(roles)
        self.acl.add(struct)
        self.acl.grants(grants)

    def check_any(self, resource, permission, roles=None):
        """
        Check if any of the provided roles have access to this resource /
        permission combination. Returns True if at least one role has access,
        False otherwise

        Arguments:
        resource -- the resource to check
        permission -- the permission to check
        roles -- a list of roles (default: None)
        """
        if roles is None:
            roles = self._determine_roles()
        return self.acl.check_any(roles, resource, permission)

    def check_all(self, resource, permission, roles=None):
        """
        Check if all provided roles have access to this resource / permission
        combination. Returns True if all roles have access, False otherwise.

        Arguments:
        resource -- the resource to check
        permission -- the permission to check
        roles -- a list of roles (default: None)
        """
        if roles is None:
            roles = self._determine_roles()
        return self.acl.check_all(roles, resource, permission)

    def set_current_roles(self, roles):
        """
        Sets the current roles to be used in check_any or check_all if no
        specific roles are provided

        Arguments:
        roles -- the list of roles
        """
        if not isinstance(roles, list):
            raise TypeError()

        self._current_roles = roles

    def set_roles_callback(self, func):
        """
        Specify a function that will be called to determine the current roles
        on a check call if no specific roles have be assigned to that call.

        Arguments:
        func -- the function handle to call
        """
        self._roles_callback = func

    def _determine_roles(self):
        """
        Determine the currently valid roles
        """
        if self._roles_callback is not None:
            return self._roles_callback()
        else:
            return self._current_roles

    def __str__(self):  # pragma: no cover
        return str(self.acl.__getstate__())

    def get_error_message(self):
        """
        Returns the error message to be returned by the decorators
        """
        return self.app.config.get('MACL_ERROR_MESSAGE', 'You do not have access to this resource')
