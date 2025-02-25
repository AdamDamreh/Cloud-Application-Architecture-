import os
import requests
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from dotenv import load_dotenv


def main():
    load_dotenv()
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")

    if not api_key:
        raise ValueError("Could not find API Key.")
        print("Can't find key")
        return
    stock_symbol = input("Enter a stock symbol for monitoring (AAPL, TSLA, IBM): ").strip().upper()
    endpoint = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock_symbol,
        "apikey": api_key,
        "outputsize": "compact"
        }

    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise HTTPError if status != 200
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making request: {e}")
        return

    # Parse JSON
    data = response.json()
    time_series = data.get("Time Series (Daily)", None)
    # Check if valid data was returned
    if "Time Series (Daily)" not in data:
        print("Unexpected data format received. Check API parameters and usage limits.")
        return
    if not time_series:
       print("No data")
       return

       dates = []
       closing_prices = []
       sorted_dates = sorted(time_series.keys())

    time_series = data["Time Series (Daily)"]

    # Extract dates and closing prices
    dates = sorted(time_series.keys())  # Sort dates (oldest first)
    closing_prices = [float(time_series[date]["4. close"]) for date in dates]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(dates, closing_prices, marker='o', linewidth=1, label=stock_symbol)
    plt.title(f"{stock_symbol} Stock Price (Daily Close)")
    plt.xlabel("Date")
    plt.ylabel("Closing Price (USD)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
