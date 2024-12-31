Cisco SDWAN - REST-API Scripts
------------------------------

Cisco SD-WAN does not support your standard REST API calls.  Instead, an HTTP session must be established AND client token must be obtained & added to the session headers BEFORE any API calls are made.

Session Creation:
- sdWanAuthentication.py creates an HTTP session, obtains token, adds token to session headers, and RETURNS the session.

Interacting with vManage using session obtained from sdWanAuthentication.py:
- Look at sdWanGetDevices.py. I leverage the returned session from sdWanAuthentication.py to then write a function that allows me to interact with vManage.
- The runnable script is actually sdWanTestScript.py, where I call sdWanGetDevices.py.

That is all.
