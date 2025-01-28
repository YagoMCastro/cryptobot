from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import schedule
import time
from threading import Thread
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

if not BOT_TOKEN or not CHAT_ID:
    raise ValueError("BOT_TOKEN or CHAT_ID is missing in the environment variables!")

print(f"Chat ID: {CHAT_ID}")
print(f"Bot Token: {BOT_TOKEN}")

BINANCE_API_PRICE_URL = "https://api.binance.com/api/v3/ticker/price"
BINANCE_API_INFO_URL = "https://api.binance.com/api/v3/exchangeInfo"

# Function to get crypto price from Binance
def get_crypto_price(symbol: str) -> str:
    try:
        response = requests.get(BINANCE_API_PRICE_URL, params={"symbol": symbol})
        response.raise_for_status()  # Raise HTTP errors if any
        data = response.json()

        if "price" in data:
            price = float(data["price"])
            return f"The current price of {symbol} is ${price:.2f}."
        elif "code" in data and data["code"] == -1121:  # Invalid symbol error
            return f"Error: {symbol} is not a valid cryptocurrency symbol."
        else:
            return "Error: Unable to fetch price. Please try again later."
    except Exception as e:
        return f"Error fetching price: {e}"


async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    '''
    Command handler for /price
    '''
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /price <symbol>. Example: /price BTCUSDT")
        return

    symbol = args[0].upper()  # Convert input to uppercase (e.g., BTCUSDT)
    message = get_crypto_price(symbol)
    await update.message.reply_text(message)

def get_btc_price() -> float:
    get_crypto_price('BTCUSDT')

async def btc_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    price = get_crypto_price("BTCUSDT")
    await update.message.reply_text(price)

async def send_daily_btc_price(application):
    try:
        price = get_btc_price()
        if price > 0:
            await application.bot.send_message(
                chat_id=CHAT_ID, text=f"Daily BTC price: ${price:,.2f}"
            )
        else:
            print("Failed to fetch BTC price for daily message.")
    except Exception as e:
        print(f"Error sending daily BTC price: {e}")

def schedule_daily_message(application):
    schedule.every().day.at("09:00").do(
        lambda: application.create_task(send_daily_btc_price(application))
    )
    while True:
        schedule.run_pending()
        time.sleep(1)


async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Your Chat ID is: {chat_id}")
    print(f"Chat ID: {chat_id}")  # Log to console


def list_binance_cryptos() -> str:
    """
    Fetches the first 20 cryptocurrencies available on Binance
    and formats them as 'CoinName - Symbol'.
    
    Returns:
        str: A formatted message listing the first 20 cryptocurrencies.
    """
    BINANCE_API_DOC = "https://binance-docs.github.io/apidocs/spot/en/#exchange-information"
    try:
        # Make a request to the Binance API
        response = requests.get(BINANCE_API_INFO_URL)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        # Get the first 20 base assets and their symbols
        unique_cryptos = []
        for symbol_info in data["symbols"]:
            base_asset = symbol_info["baseAsset"]
            symbol = symbol_info["symbol"]

            # Avoid duplicates in the list (e.g., BTC appears in multiple trading pairs)
            if base_asset not in unique_cryptos:
                unique_cryptos.append(f"{base_asset}")
            
            # Stop after collecting 20 unique coins
            if len(unique_cryptos) == 20:
                break

        # Format the response message
        formatted_list = "\n".join(unique_cryptos)
        return (
            f"Here are the first 20 cryptocurrencies available:\n\n"
            f"{formatted_list}\n\n"
            f"For the full list, check the Binance API documentation: {BINANCE_API_DOC}"
        )

    except Exception as e:
        return f"Error fetching cryptocurrencies: {e}"

async def list_cryptos(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    symbols = list_binance_cryptos()
    await update.message.reply_text(symbols)

if __name__ == "__main__":
    # Build the Telegram application
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add command handlers
    app.add_handler(CommandHandler("chatid", get_chat_id))
    app.add_handler(CommandHandler("btcprice", btc_price))
    app.add_handler(CommandHandler("price", price))
    app.add_handler(CommandHandler("listcryptos", list_cryptos))

    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=schedule_daily_message, args=(app,), daemon=True)
    scheduler_thread.start()

    # Start the bot
    print("Bot is running...")
    app.run_polling()
