import requests
import json
from auth_settings import *
url=base_url+'voyages2022_auth_endpoint/'
r=requests.post(url,{'username':'voyages','password':'voyages'})
token=json.loads(r.text)['token']

headers={'Authorization':'Token %s' %token}

print(headers)