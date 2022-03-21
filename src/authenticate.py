import requests
import json
from auth_settings import *
url=base_url+'voyages2022_auth_endpoint/'
r=requests.post(url,{'username':username,'password':password})

try:
	token=json.loads(r.text)['token']
	auth_headers={'Authorization':'Token %s' %token}
except:
	auth_headers=None
	print(r.text)