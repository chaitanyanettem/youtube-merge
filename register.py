import requests
import config
import time
import traceback
import sys

initial_payload = {"client_id":config.client_id, "scope":config.scope} 
#config contains variables client_id and scope. Suitably create a config.py file in the same 
#PATH as this script
access_token = open(".access_token","w+")
refresh_token = open(".refresh_token","w+")

response = requests.post("https://accounts.google.com/o/oauth2/device/code", initial_payload)
url = response.json()['verification_url']
code = response.json()['user_code']
poll_interval = response.json()['interval']
print "Please visit {url} and enter this code: {code}".format(url=url,code=code)
print response.text

poll_payload = {"client_id": config.client_id, "scope":config.scope, "client_secret":config.client_secret, "code":code, "grant_type":"http://oauth.net/grant_type/device/1.0"}
flag = 0
while True:
	if flag == 0:
		flag = 1
		sys.stdout.write("\rWaiting for response...")
		sys.stdout.flush()
	elif flag == 1:
		flag = 0
		sys.stdout.write("\rWaiting for response   ")
		sys.stdout.flush()
	poll_response = requests.post("https://accounts.google.com/o/oauth2/token", poll_payload)
	try:
		if poll_response.json()['error'] == 'authorization_pending':
			time.sleep(poll_interval)
		elif poll_response.json()['error'] == 'slow_down':
			time.sleep(poll_interval+10)
		else:
			print "Unknown error: ",poll_response.json()['error']
			break
	except KeyError:
		if poll_response.json()['access_token']:
			print "Access Token received."
			print poll_response.json()['access_token']

