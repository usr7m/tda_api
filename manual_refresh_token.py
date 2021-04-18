import os
from selenium import webdriver
import urllib.parse as up
from shutil import which
import requests
import time

''' API client_ID auth stuff: '''

client_id = 'CLIENT_ID'           # fill this out with your ID, JUST ID, nothing else. no @AMER.OA.... no, just ID
redirect_uri = 'http://Localhost'

''' chomium options and such '''

options = webdriver.ChromeOptions()
options.binary_location = which('chromium')
chrome_driver_binary = '/PATH_TO/chromedriver'   # you will need a chromedriver for this (easily obtained), or work around manually
driver = webdriver.Chrome(chrome_driver_binary, options=options)

url = 'https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=' 
        + redirect_uri\
	      + '&client_id=' 
        + client_id 
        + '%40AMER.OAUTHAP'

driver.get(url)

''' this part can be skipped
    and all forms filled out on the web as directed untill... '''
    
print('TDA username: ')     # 
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

''' until HERE .... this is where your code appears in the URL '''

''' fetch and decode the code '''

code = up.unquote(driver.current_url.split('code=')[1])
print(code)
driver.close()

''' get the access and refresh tokens via obtained code '''

resp = requests.post('https://api.tdameritrade.com/v1/oauth2/token',
                     headers={'Content-Type': 'application/x-www-form-urlencoded'},
                     data={'grant_type': 'authorization_code',
                           'refresh_token': '',
                           'access_type': 'offline',
                           'code': code,
                           'client_id': client_id,
                           'redirect_uri': redirect_uri})
print(resp.status_code)
print(resp.json())
access_token = resp.json()['access_token']
refresh_token = resp.json()['refresh_token']
token_type = resp.json()['token_type']

''' a quick function to put the refresh token into a txt file '''

def create_rtok_file(refresh_token):
	f_path = '/PATH_TO_NEW_TOKEN_FILE/'           # fill this out with your own path to file
	f = open(f_path + 'refresh_token.txt', 'w')   
	f.write(refresh_token)
	f.close()

''' call it ^ '''

create_rtok_file(refresh_token)
