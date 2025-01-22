# **Telegram BTC Price Bot**

This is a Telegram bot that uses the Binance API to monitor the price of Bitcoin (BTC) and send daily updates to a specific chat. Users can also manually check the current BTC price using a bot command.

---

## **Features**
- Fetch the current Bitcoin (BTC) price from Binance.
- Respond to the `/btcprice` command to display the current BTC price in a chat.
- Send daily BTC price updates at a specified time (default: 09:00).
- Allows users to retrieve their Telegram chat ID using the `/chatid` command.
---

## **Technologies Used**
- **Python**
- **Telegram Bot API** (via the `python-telegram-bot` library)
- **Binance API**
- **Dotenv** (for secure environment variable management)
- **Schedule** (for scheduling daily messages)
- **Threading** (to run the scheduler and bot concurrently)

---

## **Setup and Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-repo/telegram-btc-price-bot.git
cd telegram-btc-price-bot
```
### **2. Install Dependencies**
Make sure you have Python 3.7 or newer installed. Install the required Python packages:
```bash
pip install python-telegram-bot requests python-dotenv schedule
```
### **3. Set Up Environment Variables**
Create a `.env` file in the root directory:
```bash
touch .env
``` 
Add the following variables to the `.env` file:
```env
BOT_TOKEN=your_bot_token
CHAT_ID=your_chat_id
```
Replace `your_bot_token` with the Telegram bot token from *@BotFather*.
Replace `your_chat_id` with the chat ID where the daily BTC price should be sent. (Use the `/chatid` command to get your chat ID if needed.)

### **4. Run the Bot**
Start the bot with:

```bash
python bot.py
```
The bot will start polling for updates, and the daily BTC price scheduler will run in the background.

