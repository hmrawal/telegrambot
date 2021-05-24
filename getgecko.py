#import statements
import requests
import json
import time
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects

#URLs needed
baseurl = 'https://api.coingecko.com/api/v3/'
epprice = 'simple/price'

#parameters needed for URL
def param(coin, currencypair):
    parameters = {
        'ids': coin,
        'vs_currencies' : currencypair
    }
    return parameters

#headers needed for URL
headers = {
  'accept': 'application/json',
}

#Session statements
session = Session()
session.headers.update(headers)

#program logic
def displaycryptoprice(coin, currencypair):
    try:
        response = session.get(baseurl + epprice, params=param(coin, currencypair))
        data = json.loads(response.text)
        return str(data[coin][currencypair])

  
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
