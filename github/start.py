import os
import getpass

from github.client import GitHub
from github.caller import api_caller


def start_github():
    """Starts the GitHub client with an authentication session depending on
    user's choice with using a Password method or a Token-based method.
    """

    print('\nStarting GitHub client!\n')
    GITHUB_API = 'https://api.github.com'

    def auth_session_call(USERNAME, **kwargs):
        """Returns an authenticated session object based on given method.

        Method 1: Username & Password
        Method 2: Token

        Additionally, prints out the session info after method decision.
        """

        if 'PASSWORD' in kwargs:
            PASSWORD = kwargs['PASSWORD']
            auth_session = GitHub(USERNAME, PASSWORD=PASSWORD)
        elif 'API_TOKEN' in kwargs:
            API_TOKEN = kwargs['API_TOKEN']
            auth_session = GitHub(USERNAME, API_TOKEN=API_TOKEN)

        auth_session.print_session()
        return auth_session

    # Check or get username
    if os.environ.get('GITHUB_USERNAME') == '':
        print('No environmental variable found for GITHUB_USERNAME.\n')
        USERNAME = input('\nPlease enter your GitHub username: ')
    else:
        USERNAME = os.environ.get('GITHUB_USERNAME')
        print(f'GITHUB_USERNAME found, username = {USERNAME}.\n')

    # Ask user for password or token method of authentication
    try:
        pass_or_tok = input('Please enter p for password or t for token: ')
        if pass_or_tok.lower() in ['p', 't', 'true', 'false']:
            pass
        else:
            raise ValueError
    except ValueError:
        print('\nInvalid selection in response, please try again.')
    else:
        # Check for password or token option
        if pass_or_tok.lower() == 'p':
            print('\nChecking if password environmental variables exists...')
            if os.environ.get('GITHUB_PASSWORD') == '':
                print('No environmental variable found for GITHUB_PASSWORD.\n')
                PASSWORD = getpass.getpass('Please enter your password: ')
            else:
                print('\nEnvironmental variable found!\n')
                PASSWORD = os.environ.get('GITHUB_PASSWORD')

            # Returns the authenticated session to use in the api caller
            auth_session = auth_session_call(USERNAME, PASSWORD=PASSWORD)

        else:
            print('Token it is, checking if token environmental variable exists...')
            if os.environ.get('GITHUB_TOKEN') == '':
                print('No environmental variable found for GITHUB_TOKEN.\n')
                API_TOKEN = getpass.getpass('Please enter your token: ')
            else:
                print('Environmental variable found!\n')
                API_TOKEN = os.environ.get('GITHUB_TOKEN')
                # Returns the authenticated session to use in the api caller
                auth_session = auth_session_call(USERNAME, API_TOKEN=API_TOKEN)

    # Start program with the api caller
    api_caller(GITHUB_API, auth_session)
    return
