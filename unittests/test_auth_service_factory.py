import unittest
from auth_service_factory import AuthServiceFactory
from auth_service import AuthService

# Unit test for auth_service_factory
class TestAuthServiceFactory(unittest.TestCase):
    # Create service and check if it matches AuthServices
    def test_create_auth_service(self):
        service = AuthServiceFactory.create_auth_service()
        self.assertIsInstance(service, AuthService)


if __name__ == '__main__':
    unittest.main()