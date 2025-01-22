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
print(f"Chat id: {CHAT_ID}")
print(f"Bot Token: {BOT_TOKEN}")
# Binance API endpoint
BINANCE_API_URL = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

# Function to get the BTC price from Binance
def get_btc_price():
    response = requests.get(BINANCE_API_URL)
    data = response.json()
    return float(data["price"])

# Command to check BTC price manually
async def btc_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_btc_price()
    await update.message.reply_text(f"Current BTC price: ${price:,.2f}")

# Function to send daily BTC price
async def send_daily_btc_price(application):
    chat_id = cHA  # Replace with your chat ID
    price = get_btc_price()
    await application.bot.send_message(chat_id=CHAT_ID, text=f"Daily BTC price: ${price:,.2f}")

# Schedule daily messages
def schedule_daily_message(application):
    schedule.every().day.at("09:00").do(
        lambda: application.create_task(send_daily_btc_price(application))
    )
    while True:
        schedule.run_pending()
        time.sleep(1)

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Your Chat ID is: {chat_id}")
    print(f"Chat ID: {chat_id}")  # Log to console

# Main function to set up the bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()


    app.add_handler(CommandHandler("chatid", get_chat_id))

    # Add command handler
    app.add_handler(CommandHandler("btcprice", btc_price))

    # Start the scheduler in a separate thread
    scheduler_thread = Thread(target=schedule_daily_message, args=(app,))
    scheduler_thread.start()

    # Start the bot
    print("Bot is running...")
    app.run_polling()
