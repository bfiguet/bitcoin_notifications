import requests
from pprint import pprint

#bitcoin_api_url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/' #obsolete
url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  'symbol':'BTC,ETH',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'd645bbdc-197a-43d4-8a67-eb278de2bf53',
}

response = requests.get(url, params = parameters, headers = headers).json()
#pprint(response)
price = response['data']['BTC']['quote']['USD']['price']

print(price)

ifttt_webhook_url = 'https://maker.ifttt.com/trigger/test_event/with/key/o3ih0Vf3uCg8jFeiUjnbvB2cMH5tC3tvImVF9klvet9'
requests.post(ifttt_webhook_url)
ttt_bitcoin_emergency = 'https://maker.ifttt.com/trigger/bitcoin_price_emergency/with/key/o3ih0Vf3uCg8jFeiUjnbvB2cMH5tC3tvImVF9klvet9'