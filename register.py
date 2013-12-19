import requests
import config

payload = {"client_id":config.client_id, "scope":config.scope} 
#config contains variables client_id and scope. Suitably create a config.py file in the same 
#PATH as this script

response = requests.post("https://accounts.google.com/o/oauth2/device/code", payload)

print response.text