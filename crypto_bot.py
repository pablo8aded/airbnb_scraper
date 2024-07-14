import hmac
import hashlib
import time
import json
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Replace with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = '7297065030:AAEgxkeYSuucVD67Jz_Hy6luJ6zsupOasmk'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome! Use /buy to buy crypto for $5 on MEXC.')

# Replace with your actual MEXC API key and secret

# Load API keys from .env file

load_dotenv(os.sys.path[0])
#load_dotenv()
API_KEY = os.getenv('MEXC_API_KEY')
API_SECRET = os.getenv('MEXC_API_SECRET')
def create_signature(data, secret):
    return hmac.new(secret.encode(), data.encode(), hashlib.sha256).hexdigest()

def buy_crypto(update: Update, context: CallbackContext) -> None:
    symbol = 'BTCUSDT'  # Example trading pair
    quantity = 5  # Buy $10 worth of BTC
    timestamp = int(time.time() * 1000)
    
    params = {
        'symbol': symbol,
        'side': 'BUY',
        'type': 'MARKET',
        'quoteOrderQty': quantity,
        'recvWindow': 5000,
        'timestamp': timestamp
    }

    query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
    signature = create_signature(query_string, MEXC_API_SECRET)
    params['signature'] = signature

    headers = {
        'X-MEXC-APIKEY': MEXC_API_KEY
    }

    response = requests.post(f'https://api.mexc.com/api/v3/order', headers=headers, params=params)

    if response.status_code == 200:
        update.message.reply_text('Successfully bought crypto for $5!')
    else:
        update.message.reply_text(f'Failed to buy crypto: {response.json()}')

def main():
    '''updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("buy", buy_crypto))

    updater.start_polling()
    updater.idle()'''

    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes
    # Replace 'YOUR_TOKEN' with your actual bot token
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Define a simple start command handler
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text('Hello! I am your bot.')

    # Register the start command handler
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("buy", buy_crypto))
    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()

