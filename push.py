#!/usr/bin/env python
import json, os, tweetpony, httplib, urllib

"""
This script uses pushover to notify the user of mentions of his username on Twitter.
"""

TWITTER_CONSUMER_KEY = "t9zCoWf7TI74GEedUdXMrQ"
TWITTER_CONSUMER_SECRET = "w85wWDRm377enzcCUAFnB3fOU1dYWmjEjBnOCY5sE"
PUSHOVER_APP_TOKEN = "aPmJWBbrnzZVGNCQaz8G651smvN3Du"
PUSHOVER_USER_KEY = "your_user_key_here"

class StreamProcessor(tweetpony.StreamProcessor):
	def on_status(self, status):
		if username in status.text:
			push("@%s" % status.user.screen_name, status.text)
		return True

def authenticate():
	try:
		api = tweetpony.API(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)
		url = api.get_auth_url()
		print "Visit this URL to obtain your verification code: %s" % url
		verifier = raw_input("Input your code: ")
		api.authenticate(verifier)
	except tweetpony.APIError as err:
		print "Oh no! You could not be authenticated. Twitter returned error #%i and said: %s" % (err.code, err.description)
	else:
		auth_data = {'access_token': api.access_token, 'access_token_secret': api.access_token_secret}
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".auth_data.json"), 'w') as f:
			f.write(json.dumps(auth_data))
		print "Hello, @%s! You have been authenticated. You can now run this script without having to authenticate every time." % api.user.screen_name

def get_api():
	if not os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".auth_data.json")):
		authenticate()
	with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".auth_data.json"), 'r') as f:
		auth_data = json.loads(f.read())
	try:
		api = tweetpony.API(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET, auth_data['access_token'], auth_data['access_token_secret'])
	except tweetpony.APIError as err:
		print "Oh no! You could not be authenticated. Twitter returned error #%i and said: %s" % (err.code, err.description)
	else:
		return api
	return False

def push(title, message):
	conn = httplib.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
		urllib.urlencode({
			"token": PUSHOVER_APP_TOKEN,
			"user": PUSHOVER_USER_KEY,
			"title": title,
			"message": message,
		}), { "Content-type": "application/x-www-form-urlencoded" })

def main():
	api = get_api()
	if not api:
		return
	processor = StreamProcessor(api)
	global username
	username = api.user.screen_name
	try:
		print "The script is now running. It *should* work."
		api.user_stream(processor = processor)
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()
