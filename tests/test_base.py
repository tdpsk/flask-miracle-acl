from flask_miracle import Acl
import unittest


class TestBaseClass(unittest.TestCase):
    acl = None

    def setUp(self):
        self.acl = Acl()
        self.acl.load_from_dict({'roles': {'admin', 'user'},
                                 'struct': {'blog': {'post', 'read'},
                                            'product': {'post', 'read'}},
                                 'grants': {'user': {'blog': {'read'}},
                                            'admin': {'blog': {'read', 'write'}}}})

    def test_load_dict(self):
        self.acl.load_from_dict({'grants': {'user': {'blog': {'write'}}}})
        assert self.acl.check_any('blog', 'write', ['user']) is True

    def test_load_class(self):
        class AclClass():
            GRANTS = {'user': {'blog': {'write'}}}
            ROLES = ['tester']
            STRUCT = {'backend': ['read']}

        self.acl.load_from_class(AclClass)
        assert self.acl.check_any('blog', 'write', ['user']) is True

    def test_check_any(self):
        assert self.acl.check_any('blog', 'write', ['user', 'admin']) is True
        assert self.acl.check_any('blog', 'write', ['user']) is False

    def test_check_all(self):
        assert self.acl.check_all('blog', 'write', ['user', 'admin']) is False
        assert self.acl.check_all('blog', 'write', ['admin']) is True

    def test_current_roles(self):
        self.acl.set_current_roles(['user'])
        assert self.acl.check_any('blog', 'write') is False
        assert self.acl.check_any('blog', 'read') is True

        self.acl.set_current_roles(['user', 'admin'])
        assert self.acl.check_all('blog', 'write') is False
        assert self.acl.check_all('blog', 'read') is True

    def test_current_roles_invalid(self):
        with self.assertRaises(TypeError):
            self.acl.set_current_roles('not_a_list')

    def test_role_callback(self):
        def func():
            return ['admin']
        self.acl.set_roles_callback(func)
        assert self.acl.check_any('blog', 'write') is True


if __name__ == '__main__':
    unittest.main()
