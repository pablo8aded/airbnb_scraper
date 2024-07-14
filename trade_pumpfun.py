import time
import requests
from bs4 import BeautifulSoup
#from binance.client import Client

# Binance API credentials
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'

#client = Client(api_key, api_secret)

def get_new_listed_coins():
    """Scrape pump.fun for newly listed coins."""
    url = "https://pump.fun"  # Replace with actual URL if different
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract newly listed coins from the page (adjust according to actual HTML structure)
    # Here we assume the coins are in a table with class 'new-coins' and <tr> elements
    new_coins = []
    for row in soup.find_all('tr', class_='new-coin-row'):
        coin = row.find('td', class_='coin-symbol').text.strip()
        new_coins.append(coin)
    
    return new_coins

def get_current_price(symbol):
    """Get the current price of the given symbol."""
    try:
        ticker = client.get_ticker(symbol=symbol)
        return float(ticker['lastPrice'])
    except Exception as e:
        print(f"Error fetching current price: {e}")
        return None

def place_order(symbol, side, quantity):
    """Place an order to buy or sell a given quantity of the symbol."""
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        return order
    except Exception as e:
        print(f"Error placing order: {e}")
        return None

def buy_and_sell(symbol, quantity):
    """Buy the coin and sell it when the price doubles."""
    # Buy the coin
    buy_order = place_order(symbol, 'BUY', quantity)
    if not buy_order:
        return

    # Get the purchase price
    buy_price = get_current_price(symbol)
    if not buy_price:
        return

    print(f"Bought {quantity} {symbol} at {buy_price}")

    # Calculate the target sell price (double the buy price)
    target_price = buy_price * 2

    # Monitor the price and sell when it doubles
    while True:
        current_price = get_current_price(symbol)
        if current_price and current_price >= target_price:
            sell_order = place_order(symbol, 'SELL', quantity)
            if sell_order:
                print(f"Sold {quantity} {symbol} at {current_price}")
            break
        time.sleep(10)  # Wait before checking the price again

# Main bot loop
while True:
    new_coins = get_new_listed_coins()
    for coin in new_coins:
        # Assuming the symbol is in the format 'COINUSDT' for Binance
        symbol = f"{coin}USDT"
        quantity = 1  # Define the quantity you want to trade
        buy_and_sell(symbol, quantity)
    time.sleep(300)  # Check for new coins every 5 minutes