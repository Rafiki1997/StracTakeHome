import unittest
from unittest.mock import patch, MagicMock
from auth_service import AuthService

class TestAuthService(unittest.TestCase):

    @patch('auth_service.Credentials')  # Mock the Credentials class
    @patch('auth_service.os.path.exists')  # Mock os.path.exists to control the flow
    @patch('builtins.open')  # Mock file open
    def test_authenticate_with_existing_token(self, mock_open, mock_exists, mock_credentials):
        # Arrange
        mock_exists.return_value = True  # Simulate 'token.json' exists
        mock_creds = MagicMock()
        mock_creds.valid = True  # Simulate valid credentials
        mock_creds.to_json.return_value = '{"token": "fake-token"}'  # Make to_json return a string
        mock_credentials.from_authorized_user_file.return_value = mock_creds

        auth_service = AuthService()

        # Act
        creds = auth_service.authenticate()

        # Assert
        mock_credentials.from_authorized_user_file.assert_called_once_with('token.json', ['https://www.googleapis.com/auth/drive'])
        self.assertTrue(creds.valid)

    @patch('auth_service.InstalledAppFlow')  # Mock the OAuth flow
    @patch('auth_service.os.path.exists')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)  # Mock file open for writing token.json
    def test_authenticate_with_new_token(self, mock_open, mock_exists, mock_flow):
        # Arrange
        mock_exists.return_value = False  # Simulate 'token.json' doesn't exist
        mock_creds = MagicMock(valid=True)  # Simulate valid credentials after authentication
        mock_creds.to_json.return_value = '{"token": "fake-token"}'  # Make to_json return a string
        mock_flow_instance = MagicMock()
        mock_flow_instance.run_local_server.return_value = mock_creds
        mock_flow.from_client_secrets_file.return_value = mock_flow_instance

        auth_service = AuthService()

        # Act
        creds = auth_service.authenticate()

        # Assert
        mock_flow.from_client_secrets_file.assert_called_once_with('credentials.json', ['https://www.googleapis.com/auth/drive'])
        mock_open.assert_called_once_with('token.json', 'w')  # Ensure token.json is being written to
        mock_open().write.assert_called_once_with('{"token": "fake-token"}')  # Ensure the credentials are written as a string
        self.assertTrue(creds.valid)

if __name__ == '__main__':
    unittest.main()
