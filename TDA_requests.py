import json
import pandas as pd
import requests
import os

def import_credentials(auth_client_id, auth_access_token):
	global client_id, access_token
	client_id = auth_client_id
	access_token = auth_access_token


''' milliseconds since epoch ''' 

def timestamp(dt):
	return int(pd.to_datetime(dt).timestamp() * 1000)


''' set endDate to tomorrow's date to get today's candle too  '''
def historical(	symbol, 
		periodType = '',
		period = '',
		frequencyType = '',
		frequency = '',
		startDate = '', 
		endDate = '', 
		ext = 'true'):
	resp = requests.get('https://api.tdameritrade.com/v1/marketdata/' + symbol + '/pricehistory',
			headers={'Authorization': 'Bearer ' + access_token},
			params={'apikey': client_id,
				'periodType': periodType,
				'period': period,
				'frequencyType': frequencyType,
				'frequency': frequency,
				'endDate': timestamp(endDate),
				'startDate': timestamp(startDate), 
				'needExtendedHoursData': ext })
	print(resp.status_code)
	return resp.json()


def search_instruments(symbol, proj):
	'''
	# posssible projections:
	# symbol-search			symbol ex: 'SPY'
	# symbol-regex					 : 'SPY.*'		
	# desc-search					 : 'FakeCompany'
	# desc-regex					 : 'XYZ.[A-C]'
	# fundamental					 : 'SPY'
	#
	'''
	resp = requests.get('https://api.tdameritrade.com/v1/instruments',
			headers={'Authorization': 'Bearer ' + access_token},
			params={'apikey': client_id,
				'symbol': symbol,
				'projection': proj})
	'''
	# print(resp.status_code)
	# print(resp.json().keys())
	'''
	return resp.json()

def quotes(symbol):
	resp = requests.get('https://api.tdameritrade.com/v1/marketdata/quotes',
			headers={'Authorization': 'Bearer ' + access_token},
			params={'apikey': client_id,
				'symbol': symbol})
	return resp.json()


def option_chain(symbol):
	resp = requests.get('https://api.tdameritrade.com/v1/marketdata/chains',
			headers={'Authorization': 'Bearer ' + access_token},
			params={'apikey': client_id,
				'symbol': symbol,
				'contractType': 'ALL',
				'strikeCount': 100,
				'includeQuotes': 'True',
				'strategy': 'SINGLE',  
				'interval': '',
				'strike': '', 
				'range': 'ALL' ,
				'fromDate': '',
				'toDate': '',
				'volatility': '',
				'underlyingPrice': '',
				'interestRate': '',
				'daysToExpiration': '',
				'expMonth': 'ALL', 
				'optionType': 'ALL'})		
	''' {strategy}:
		
			ANALYTICAL  
		(allows use of the volatility, underlyingPrice, 
		interestRate, and daysToExpiration params 
		to calculate theoretical values)
			other options: 
		
			COVERED, VERTICAL, CALENDAR, 
			STRANGLE, STRADDLE, BUTTERFLY, 
			CONDOR, DIAGONAL, COLLAR, or ROLL. 
			Default is SINGLE.

		{range}:

			ITM: In-the-money
			NTM: Near-the-money
			OTM: Out-of-the-money
			SAK: Strikes Above Market
			SBK: Strikes Below Market
			SNK: Strikes Near Market
			ALL: All Strikes

		{exp month}

		Return only options expiring in the specified month. 
		Month is given in the three character format.
		Example: 
			'JAN'

		{option type}
	
		Type of contracts to return. 
		Possible values are:
			S: Standard contracts
			NS: Non-standard contracts
			ALL: All contracts

		{strike interval}

		Strike interval for spread strategy chains
		Example:
			2

		{strike} 

		Return options only at that strike price.
		Example:
			150.0
	'''
	return resp.json()


def get_user_principals(fields):
	resp = requests.get('https://api.tdameritrade.com/v1/userprincipals',
			headers={'Authorization': 'Bearer ' + access_token},
			params={'fields': fields})
	return resp.json()




def get_orders(account_id, status, fromDate, tillDate, order_id = ''):
	uri = 'https://api.tdameritrade.com/v1/accounts/' 
	resp = requests.get(uri + account_id + '/orders/' + order_id,
			headers={'Authorization': 'Bearer ' + access_token},
			params={'maxResults': 10,
				'fromEnteredTime' : fromDate, 	#yyyy-MM-dd
				'toEnteredTime' : tillDate,	#yyyy-MM-dd
				'status': status})
	return resp.json()


def get_transactions(account_id, t_type = 'ALL', symbol = '', startDate = '', endDate = ''):
	uri = 'https://api.tdameritrade.com/v1/accounts/' 
	resp = requests.get(uri + account_id + '/transactions',
			headers={'Authorization': 'Bearer ' + access_token},
			params={'type': t_type,
				'symbol': symbol,
				'startDate' : startDate,	#yyyy-MM-dd
				'endDate' : endDate		#yyyy-MM-dd
				})
	return resp.json()



def get_transaction_by_id(account_id, transaction_id = ''):
	uri = 'https://api.tdameritrade.com/v1/accounts/' 
	resp = requests.get(uri + account_id + '/transactions/' + str(transaction_id),
			headers={'Authorization': 'Bearer ' + access_token},
			params={})
	return resp.json()




''' fields:  posittions, orders '''
def get_accounts(fields):
	uri = 'https://api.tdameritrade.com/v1/accounts'
	resp = requests.get(uri,
			headers = {'Authorization': 'Bearer ' + access_token},
			params = {'fields': fields})
	return resp.json()




def get_watchlist(account_id = '', watchlist_id = ''):
	uri = 'https://api.tdameritrade.com/v1/accounts/' + str(account_id) +'/watchlists/' + str(watchlist_id)
	print(watchlist_id)
	resp = requests.get(uri, headers = {'Authorization': 'Bearer ' + access_token})
	return resp.json()






