'''
    flask_miracle
    -------------
    This module provides a fabric layer between the Flask framework and the
    Miracle ACL library.

    :copyright: (c) 2017 by Timo Puschkasch.
    :license: BSD, see LICENSE for more details.
'''

from .base import Acl
from .functions import check_all, check_any, set_current_roles
from .decorators import macl_check_any, macl_check_all
