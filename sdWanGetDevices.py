import json, sdWanAuthentication

def sdWanGetDevices(base_url, jusername, jpassword):
    # Retrieve session via sdWanAuthentication.py
    with sdWanAuthentication.sdWanAuthentication(base_url, jusername, jpassword) as sesh:
        devices_endpoint = '/dataservice/device'
        device_response = sesh.get(
            url='https://' + base_url + devices_endpoint,
            verify=False
        ).json()

        # Show only Device ID and Device Type
        print('='*55 + '\nDEVICE SUMMARY *** Only Device ID and Device Type ***\n' + '='*55 + '\n')
        for device in device_response['data']:
            print('Device ID: ' + device['deviceId'] + '\nDevice Type: ' + device['device-type'] + '\n ++++\n')

        # Print out entire json formatted device data
        print('\n\n' + '='*50 + '\nDetailed JSON-Formatted Data\n' + '='*50)
        print(json.dumps(device_response, indent=4))
