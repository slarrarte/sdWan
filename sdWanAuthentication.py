# Cisco SD-WAN Authentication Script
import requests
from getpass import getpass

def sdWanAuthentication(base_url, jusername, jpassword):
    # Authentication Info
    requests.packages.urllib3.disable_warnings()
    auth_endpoint = '/j_security_check'
    login_body = {
        'j_username': jusername,
        'j_password': jpassword
    }

    # Session Creation
    sesh = requests.session()
    login_response = sesh.post(
        url='https://' + base_url + auth_endpoint,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data=login_body,
        verify=False
    )

    # Code stoppage if login does not succeed
    if not login_response.ok or login_response.text:
        print('Login failed')
        import sys
        sys.exit(1)
    else:
        print('Login succeeded\n\n******************************\n')
        print(login_response)
        print('\n')

    # Endpoint for retrieving client token
    token_endpoint = '/dataservice/client/token'

    # Update token to session headers
    login_token = sesh.get(
        url='https://' + base_url + token_endpoint,
        headers={'Content-Type': 'application/json'},
        verify=False
    )

    # Add Cross-Site Reference Token to session headers
    if login_token.status_code == 200:
        if b'<html>' in login_token.content:
            print("Login Token Failed")
            exit(0)
        sesh.headers['X-XSRF-TOKEN'] = login_token.content

    # Return session object to be used in other scripts
    return sesh
