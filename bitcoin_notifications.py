import requests
import os
import time
# from datetime import datetime
from dotenv import load_dotenv  # for acces to .env
import pywhatkit
# !!in terminal xhost + if some error
# !!the transmitted text is written in qwerty even if your keyboard is
# in azerty no emoji
# you need to open whatsapp web and connect you before

load_dotenv()

# will first look for a .env file and
# if it finds one, it will load the environment variables
# from the file and make them accessible to your project

PARAM = {
  'symbol': 'BTC,ETH',
  'convert': 'USD'
}
HEAD = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': os.getenv('API_KEY'),
}

REF_PRICE_BTC = float(os.getenv('BITCOIN_PRICE_THRESHOLD'))
PHONE = os.getenv('PHONE_NUM')


def get_lastest_bitcoin_price():
    response = requests.get(
        os.getenv('BITCOIN_API_URL'),
        params=PARAM, headers=HEAD
    ).json()
    price = response['data']['BTC']['quote']['USD']['price']
    return (price)


def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    return '<br>'.join(rows)


def main():
    # bitcoin_history = []
    while True:
        price = get_lastest_bitcoin_price()
        # date = datetime.now()
        # bitcoin_history.append({'date': date, 'price': current_price})

        if price < REF_PRICE_BTC:
            message = f"Alert! Bitcoin price is falling to {price:.2f}$"
            pywhatkit.sendwhatmsg_instantly(PHONE, message)

        if (price < (REF_PRICE_BTC - 5000) or price > (REF_PRICE_BTC + 5000)):
            message = f"Becarful Bitcoin price move to {price:.2f}"
            pywhatkit.sendwhatmsg_instantly(PHONE, message)

        # if len(bitcoin_history) == 5:
        #    tab = format_bitcoin_history(bitcoin_history)
        #    message = f"bitcoin_price_update {tab}"
        #    pywhatkit.sendwhatmsg_instantly(PHONE, message)          
        #    bitcoin_history = []

        time.sleep(5 * 60)


if __name__ == '__main__':
    main()
