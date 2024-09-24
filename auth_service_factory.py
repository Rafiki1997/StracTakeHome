from auth_service import AuthService

class AuthServiceFactory:
    @staticmethod
    def create_auth_service():
        return AuthService()
