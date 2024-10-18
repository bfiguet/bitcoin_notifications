import requests
import time
from datetime import datetime

BITCOIN_PRICE_THRESHOLD = 60000
BITCOIN_API_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/test_event/with/key/o3ih0Vf3uCg8jFeiUjnbvB2cMH5tC3tvImVF9klvet9'
PARAM = {
  'symbol':'BTC,ETH',
  'convert':'USD'
}
HEAD = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'd645bbdc-197a-43d4-8a67-eb278de2bf53',
}

def get_lastest_bitcoin_price():
	response = requests.get(BITCOIN_API_URL, params = PARAM, headers = HEAD).json()
	price = response['data']['BTC']['quote']['USD']['price']
	return (price)

def post_ifttt_webhook(event, value):
	data = {'value1': value}
	ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
	requests.post(ifttt_event_url, json=data)

def format_bitcoin_history(bitcoin_history):
	rows = []
	for bitcoin_price in bitcoin_history:
		date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
		price = bitcoin_price['price']
		#<b> (bold) tag creates bolded text
		row = '{}: $<b>{}</b>'.format(date, price)
		rows.append(row)
	
	#Use a <br> (break) tag to create a new line
	return '<br>'.join(rows)

def main():
	bitcoin_history = []
	while True:
		price = get_lastest_bitcoin_price()
		date = datetime.now()
		bitcoin_history.append({'date':date, 'price':price})
	
		if price < BITCOIN_PRICE_THRESHOLD:
			post_ifttt_webhook('bitcoin_price_emergency', price)

		if len(bitcoin_history) == 5:
			post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
			bitcoin_history = []

		time.sleep(5 * 60)

if __name__ == '__main__':
	main()

