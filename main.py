from authenticator import authenticate
from operations import authenticate, createGUI

def main():
    service = authenticate()
    if service:
        # If authentication was successful, create GUI
        createGUI(service)

if __name__ == "__main__":
    main()