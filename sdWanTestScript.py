import sdWanGetDevices, json
from pathlib import Path

# Import SD-WAN lab data, which is in a JSON file
data = json.load(
    open(Path.home()/'')
)

sdWanGetDevices.sdWanGetDevices(
    data['vmanage']['ipAddr'],
    data['vmanage']['username'],
    data['vmanage']['password']
)
