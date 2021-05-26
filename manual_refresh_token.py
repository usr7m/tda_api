import os
from selenium import webdriver
import urllib.parse as up
from shutil import which
import requests
import time

''' API client_ID auth stuff: '''
client_id = 'CLIENT_ID' # fill this out
path_to_token_file = '/path/to/token.file'
redirect_uri = 'https://Localhost'


options = webdriver.ChromeOptions()
options.binary_location = which('chromium')
chrome_driver_binary = '/path/to/chromedriver'
driver = webdriver.Chrome(chrome_driver_binary, options=options)

url = 'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=' + redirect_uri\
	+ '&client_id=' + client_id + '%40AMER.OAUTHAP'

driver.get(url)

print('TDA username: ')
tdauser = input()
print('TDA password: ')
tdapass = input()
ubox = driver.find_element_by_id('username0')
pbox = driver.find_element_by_id('password')
ubox.send_keys(tdauser)
pbox.send_keys(tdapass)
driver.find_element_by_id('accept').click()
time.sleep(3)
driver.find_element_by_id('accept').click()
print('enter the txt code: ')	
sms_code = input()
smscodebox = driver.find_element_by_id('smscode0')
smscodebox.send_keys(sms_code)
driver.find_element_by_id('accept').click()
driver.find_element_by_id('trustthisdevice0_0').click()
driver.find_element_by_id('accept').click()

code = up.unquote(driver.current_url.split('code=')[1])
driver.close()


print(code)



def get_today_timestamp():
   today = datetime.date.today()
   today = pd.to_datetime(today).timestamp()
   return int(today)


def both_tokens_by_code(client_id, code):
   resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token',
                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                     data={'grant_type': 'authorization_code',
                           'refresh_token': '',
                           'access_type': 'offline',
                           'code': code,
                           'client_id': client_id,
                           'redirect_uri': redirect_uri})
   return (resp.json())


def update_tokens_by_code():
   tokens = both_tokens_by_code(client_id, code)
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
   print('token_file created.')
