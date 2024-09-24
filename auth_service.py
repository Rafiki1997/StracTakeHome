import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Define the scopes for Google Drive API access
SCOPES = ['https://www.googleapis.com/auth/drive']

# Implement AuthService as singleton to make sure only 1 instance exists
class AuthService:
    def __init__(self):
        self.creds = None

    def authenticate(self):
        # Check if the token.json file exists and check if it contains credentials
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If there are no valid credentials, prompt the user to log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)  # Assign to self.creds

            # Save the credentials for future use
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        return self.creds  # Return credentials
