import unittest
from auth_service_factory import AuthServiceFactory
from auth_service import AuthService


class TestAuthServiceFactory(unittest.TestCase):

    def test_create_auth_service(self):
        service = AuthServiceFactory.create_auth_service()
        self.assertIsInstance(service, AuthService)


if __name__ == '__main__':
    unittest.main()