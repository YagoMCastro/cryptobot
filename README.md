# **Cryptobot**

This is a Telegram bot that uses the Binance API to monitor the price of Bitcoin (BTC) and send daily updates to a specific chat. Users can also manually check the current BTC price using a bot command.

---

## **Features**
- Fetch the current Bitcoin (BTC) price from Binance.
- Respond to the `/btcprice` command to display the current BTC price in a chat.
- Send daily BTC price updates at a specified time (default: 09:00).
- Allows users to retrieve their Telegram chat ID using the `/chatid` command.
---

## **Technologies Used**
- **Telegram Bot API** (via the `python-telegram-bot` library)
- **Binance API**
- **Dotenv** (for secure environment variable management)
- **Schedule** (for scheduling daily messages)
- **Threading** (to run the scheduler and bot concurrently)

---

## **Setup and Installation**

### **1. Clone the Repository**
```
git clone https://github.com/your-repo/telegram-btc-price-bot.git
cd telegram-btc-price-bot
```
### **2. Install Dependencies**
Make sure you have Python 3.7 or newer installed. Install the required Python packages:
```
pip install python-telegram-bot requests python-dotenv schedule
```
### **3. Set Up Environment Variables**
Create a `.env` file in the root directory:
```
touch .env
``` 
Add the following variables to the `.env` file:
```
BOT_TOKEN=your_bot_token
CHAT_ID=your_chat_id
```
Replace `your_bot_token` with the Telegram bot token from *@BotFather*.
Replace `your_chat_id` with the chat ID where the daily BTC price should be sent. (Use the `/chatid` command to get your chat ID if needed.)

### **4. Run the Bot**
Start the bot with:

```
python crypto_bot.py
```
The bot will start polling for updates, and the daily BTC price scheduler will run in the background.

## **Usage**

### **1. Commands**
- **`/chatid`**: Get the chat ID of the current conversation. This is useful for setting the `CHAT_ID` environment variable.
- **`/btcprice`**: Fetch the current Bitcoin price from Binance and display it in the chat.

### **2. Daily BTC Price Updates**
The bot automatically sends the BTC price to the specified chat (`CHAT_ID`) every day at 09:00.

## **Customization**
- **Change the daily message time**:
   Modify the `schedule_daily_message` function in the code:
   ```python
   schedule.every().day.at("09:00").do(...)
   ```

## **Security Tips**
1. **Do not hardcode sensitive data** (like your bot token or chat ID) in the code. Always use environment variables.
2. Ensure that your `.env` file is added to `.gitignore` to prevent it from being uploaded to version control.
## **Troubleshooting**
- If the bot doesn’t respond:
   - Check that the `BOT_TOKEN` is valid and correctly set in the `.env` file.
   - Ensure the bot is added to the intended Telegram chat.
- If the daily BTC price isn’t sent:
   - Verify the `CHAT_ID` in the `.env` file.
   - Check that the bot is running and the scheduler thread is active.

## **License**
This project is licensed under the MIT License. See the `LICENSE` file for details.

## **Contributing**
Feel free to fork this repository and submit pull requests for improvements or new features!


