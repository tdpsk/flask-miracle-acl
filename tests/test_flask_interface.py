from flask import Flask, current_app
from flask_miracle import Acl, macl_check_any, macl_check_all
import unittest

class TestFlaskInterface(unittest.TestCase):
    def setUp(self):
        class AclClass():
            STRUCT = {
                'blog': ['read', 'write', 'delete']
            }

            GRANTS = {
                'user': {
                    'blog': ['read']
                },
                'admin': {
                    'blog': ['read', 'write']
                }
            }

        self.app = Flask(__name__)
        self.app.config['MACL_DEFINITION'] = {'roles': ['user', 'admin']}
        self.app.config['MACL_CLASS'] = AclClass
        self.app.config['MACL_DEFAULT_ROLES'] = ['user']
        self.acl = Acl(self.app)
        self.client = self.app.test_client()

    def test_setup(self):
        self.acl.set_current_roles(['user', 'admin'])
        assert self.acl.check_any('blog', 'write') is True
        assert self.acl.check_all('blog', 'write') is False

    def test_default_roles(self):
        assert self.acl.check_any('blog', 'read') is True
        assert self.acl.check_any('blog', 'write') is False

    def test_decorators(self):
        self.acl.set_current_roles(['user', 'admin'])

        @self.app.route('/any_forbidden')
        @macl_check_any('blog', 'delete')
        def any_forbidden():
            return 'allowed'

        @self.app.route('/any_allowed')
        @macl_check_any('blog', 'write')
        def any_allowed():
            return 'forbidden'

        @self.app.route('/all_forbidden')
        @macl_check_all('blog', 'write')
        def all_forbidden():
            return 'forbidden'

        @self.app.route('/all_allowed')
        @macl_check_all('blog', 'read')
        def all_allowed():
            return 'allowed'

        response = self.client.get('/any_forbidden')
        assert response.status_code == 403
        response = self.client.get('/all_forbidden')
        assert response.status_code == 403
        response = self.client.get('/any_allowed')
        assert response.status_code == 200
        response = self.client.get('/all_allowed')
        assert response.status_code == 200


    def test_functions(self):
        @self.app.route('/')
        def hello():
            from flask_miracle import check_any, check_all, set_current_roles
            set_current_roles(['user', 'admin'])
            return 'check any: {}; check all: {}'.format(check_any('blog', 'write'), check_all('blog', 'write'))

        response = self.client.get('/')
        data = response.data.decode('utf-8')
        assert response.status_code == 200
        assert data == 'check any: True; check all: False'
