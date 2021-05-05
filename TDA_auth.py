import json
import pandas as pd
import datetime
import os
import requests

client_id = 'CLIENT_ID' # fill this out with your API client_ID
path_to_token_file = '/path/to/token_file/' # fill this out with path to your token file

# print(os.getcwd())

def read_tokens_from_file():
	global refresh_token, refresh_token_expiry
	try:
		with open(path_to_token_file + 'token_file', 'r') as token_file:
			tokens = json.load(token_file) 
	except FileNotFoundError:
		print('404')
		print('create token file first')
	print(json.dumps(tokens, indent = 4))
	refresh_token = tokens['refresh_token']
	refresh_token_expiry =\
		pd.to_datetime(tokens['refresh_token_expires_ON'], 
						unit = 's')
	return refresh_token, refresh_token_expiry


def both_tokens_by_refresh(refresh_token, client_id):
	resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token',
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data={'grant_type': 'refresh_token',
                               'refresh_token': refresh_token,
                               'access_type': 'offline',
                               'code': '',
                               'client_id': client_id,
                               'redirect_uri': ''})
	return (resp.json())

def access_by_refresh(refresh_token, client_id):
	global access_token
	resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token',
                         headers={'Content-Type': 'application/x-www-form-urlencoded'},
                         data={'grant_type': 'refresh_token',
                               'refresh_token': refresh_token,
                               'access_type': '',
                               'code': '',
                               'client_id': client_id,
                               'redirect_uri': ''})
	access_token = resp.json()['access_token']

def get_today_timestamp():
	today = datetime.date.today()
	today = pd.to_datetime(today).timestamp()
	return int(today)

def update_token_file_by_refresh():
	tokens = both_tokens_by_refresh(refresh_token, client_id)
	if 'access_token' in tokens:
		del tokens['access_token']
		del tokens['expires_in']
	today = get_today_timestamp()
	refresh_token_expires_in = tokens['refresh_token_expires_in']
	refresh_token_expires_ON = int(today + refresh_token_expires_in)	
	print(refresh_token_expires_ON)
	tokens['refresh_token_expires_ON'] = refresh_token_expires_ON
	with open(path_to_token_file + 'token_file', 'w') as token_file:
		json.dump(tokens, token_file) 

def check_if_still_good():
	today = pd.to_datetime(get_today_timestamp(), unit = 's')
	time_remaining = refresh_token_expiry - today
	if time_remaining.days > 2:
		print('still time')
	else:
		print('get a new refresh_token')
		update_token_file_by_refresh()
		print('updated, try again...')
		quit()


def authenticate():
	read_tokens_from_file()
	check_if_still_good()
	access_by_refresh(refresh_token, client_id)




