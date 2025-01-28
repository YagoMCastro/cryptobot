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

# Command handler for /price
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = context.args
    if not args:
        await update.message.reply_text("Usage: /price <symbol>. Example: /price BTCUSDT")
        return

    symbol = args[0].upper()  # Convert input to uppercase (e.g., BTCUSDT)
    message = get_crypto_price(symbol)
    await update.message.reply_text(message)

# Function to fetch BTC price (used for daily notifications)
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

# Schedule daily messages
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
    Fetches the first 20 trading pair symbols from the Binance API and provides a link to the full list.

    Returns:
        str: A formatted message containing the first 20 cryptos following its symbols and the API link.
    """
    BINANCE_API_DOC = "https://binance-docs.github.io/apidocs/spot/en/#exchange-information"
    try:
        response = requests.get(BINANCE_API_INFO_URL)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()

        # Extract the first 20 trading pairs
        symbols = [
            f"{symbol_info['baseAsset']} - {symbol_info['symbol']}"
            for symbol_info in data["symbols"][:20]
        ]

        # Format the response
        formatted_symbols = "\n".join(symbols)
        return (
            f"The first 20 available cryptos:\n\n{formatted_symbols}\n\n"
            f"Explore the full list of trading pairs here: {BINANCE_API_DOC}"
        )
    except Exception as e:
        return f"Error fetching symbols: {e}"

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
    app.add_handler(CommandHandler("listsymbols", list_cryptos))

    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=schedule_daily_message, args=(app,), daemon=True)
    scheduler_thread.start()

    # Start the bot
    print("Bot is running...")
    app.run_polling()
