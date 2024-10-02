# Interacting with Cisco SD-WAN's Admin API

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
login_response = sesh.post(url=f"{base_url}{auth_endpoint}", data=login_body, verify=False)

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
login_token = sesh.get(url=f"{base_url}{token_endpoint}", verify=False)

if login_token.status_code == 200:
    if b'<html>' in login_token.content:
        print("Login Token Failed")
        exit(0)
    sesh.headers['X-XSRF-TOKEN'] = login_token.content

# ===================================================================

# Create an account that is a member of the netadmin group

admin_endpoint = 'dataservice/admin/user'

payload = {
    'group': ['netadmin'],
    'description': '',
    'userName': '',
    'password': ''
}

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

res = sesh.post(url=f'{lab["host"]}{admin_endpoint}', headers=headers, data=json.dumps(payload), verify=False)
print(res.text)

# Modify already-created account
#
# passwordEndpoint = 'dataservice/admin/user/slarrarte'
#
# payload2 = {
#     'group': ['netadmin'],
#     'description': '',
#     'userName': '',
#     'password': ''
# }
#
# res2 = sesh.put(url=f'{lab["host"]}{passwordEndpoint}', headers=headers, data=json.dumps(payload2), verify=False)
# print(res2.text)
