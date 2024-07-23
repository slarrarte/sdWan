import json
import requests
import env_lab_sdWan
import sys

# Set to either alwaysOn or reservable
labEnv = 'reservable'

if labEnv == 'alwaysOn':
    lab = env_lab_sdWan.vManageAlwaysOn
elif labEnv == 'reservable':
    lab = env_lab_sdWan.vManageReserved
else:
    print('Please set labEnv variable to either \'alwaysOn\' or \'reservable\'')
    sys.exit()


# AUTHENTICATION TO vMANAGE
# ====================================================================================

requests.packages.urllib3.disable_warnings()

base_url = lab['host']
auth_endpoint = "j_security_check"

# Login creds
login_body = {
    "j_username": lab['username'],
    "j_password": lab['password']
}

# Creating a session allows us to make multiple interactions with vManage
# while needing only to authenticate once.
sesh = requests.session()

# Create session
login_response = sesh.post(
    url=f"{base_url}{auth_endpoint}",
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
token_endpoint = 'dataservice/client/token'

# Update token to session headers
login_token = sesh.get(
    url=f"{base_url}{token_endpoint}",
    verify=False
)

if login_token.status_code == 200:
    if b'<html>' in login_token.content:
        print("Login Token Failed")
        exit(0)
    sesh.headers['X-XSRF-TOKEN'] = login_token.content

# DEEPER API CALLS
# ====================================================================================

# Get list of devices
# device_endpoint = "dataservice/device/"
#
# device_response = sesh.get(url=f"{base_url}{device_endpoint}", verify=False).json()
#
# # Just me printing out what I want to see, which is Device ID and Device Type
# # for device in device_response['data']:
# #     print('Device ID: ' + device['deviceId'] + '\nDevice Type: ' + device['device-type'] + '\n ++++\n')
#
# # Print out entire json formatted response
# print(json.dumps(device_response, indent=4))

# ---------------------------------------------

