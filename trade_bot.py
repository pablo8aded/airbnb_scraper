import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv
import schedule
from pyrogram import Client, filters
from dotenv import load_dotenv
import os

# Load API keys from .env file



# Function to generate signature
def sign(params):
    query_string = urlencode(params)
    return hmac.new(API_SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

# Function to place a market order
def place_market_order(symbol, side, quantity):
    endpoint = '/api/v3/order'
    url = BASE_URL + endpoint

    params = {
        'symbol': symbol,
        'side': side,
        'type': 'MARKET',
        'quoteOrderQty': quantity,
        'timestamp': int(time.time() * 1000)
    }
    params['signature'] = sign(params)

    headers = {
        'X-MEXC-APIKEY': API_KEY
    }

    response = requests.post(url, headers=headers, params=params)
    print(response.json())

if __name__ == "__main__":

    load_dotenv(os.sys.path[0])
    #load_dotenv()
    API_KEY = os.getenv('MEXC_API_KEY')
    API_SECRET = os.getenv('MEXC_API_SECRET')

    # Define the base URL for MEXC API
    BASE_URL = 'https://api.mexc.com'

    '''load_dotenv()

    CONFIG = {
        "telegram_api_id": int(os.getenv("TG_API_ID")),
        "telegram_hash": os.getenv("TG_API_HASH"),
    }'''

    #app = Client("my_account",CONFIG["telegram_api_id"],CONFIG["telegram_hash"])
    #channel_username = 'cryptoclubpump'
    

    #chat_id = -1001625691880

    '''async def main():
        async with app:
            async for message in app.get_chat_history(chat_id):
                me = await app.get_me() 
                print(me)
            #print(message.text)
    #print(message)
    app.run(main())'''
    
    #me = await app.get_me() 
    #print(me)
    #Target=-1001625691880

    '''@app.on_message(filters.chat(Target))
    async def handle_message(client, message):
        # Print message to console or handle as needed
        current_time = time.strftime("Current time: %H:%M:%S")
        print(current_time)
        print(message)
        symbol=message.text + 'USDT'
        print(symbol)
        chat_member = await app.get_chat_member(chat_id, 'me')
            
        # Check if the bot is an administrator
        if chat_member.status == 'administrator':
            # Check if the bot has permission to read message history
            if chat_member.can_retrieve_messages:
                print("The bot can read the message history.")
            else:
                print("The bot cannot read the message history.")
        else:
            print("The bot is not an administrator.")

    

    #app.run()
    app.run()'''
    #with app:
    #  app.send_message("me", "Hello from pyrogram")


    # Replace these with your own values
    '''api_id = '29823838'
    api_hash = '4efb12c0e476f76a8395d05342a5427d'
    channel_username = 'PreisKing

    @app.on_message(filters.chat(channel_username))
    def handle_message(client, message):
        # Print message to console or handle as needed
        print(f"New message from {channel_username}: {message.text}")
    
    app.run()'''

    symbol = 'USDT'  # Replace with the actual symbol
    side = 'BUY'
    #symbol=message.text + 'USDT'
    quote_order_qty = '10'   # Replace with the actual quantity
    current_time = time.strftime("Current time: %H:%M:%S")
    print(current_time)
    place_market_order(symbol, side, quote_order_qty)