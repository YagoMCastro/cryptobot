import requests
import time

def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    params = {"symbol": "BTCUSDT"}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
        data = response.json()
        return float(data['price'])
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def monitor_btc_price(interval=10):
    print("Monitoring BTC price...")
    while True:
        price = get_btc_price()
        if price is not None:
            print(f"BTC/USDT Price: ${price:.2f}")
        time.sleep(interval)

# Monitor BTC price every 10 seconds
monitor_btc_price(interval=10)
