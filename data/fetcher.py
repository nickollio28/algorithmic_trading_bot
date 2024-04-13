import requests
import os
from dotenv import load_dotenv
import time
import logging
import pandas as pd

load_dotenv()  # Take environment variables from .env.
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataFetcher:
    def __init__(self):
        self.stock_api_url = 'https://finnhub.io/api/v1/stock/candle'
        self.news_api_url = 'https://newsapi.org/v2/everything'
        self.api_key_finnhub = os.getenv('FINNHUB_API_KEY')
        self.api_key_newsapi = os.getenv('NEWSAPI_KEY')
    
    def fetch_data_with_retry(self, url, params, retries=5, backoff_factor=0.3):
        """Fetch data with retries and exponential backoff."""
        for attempt in range(retries):
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()  # Will raise an HTTPError for bad responses
                return response.json()
            except requests.exceptions.HTTPError as errh:
                logging.error(f"HTTP Error: {errh}")
                if response.status_code < 500:
                    raise  # Don't retry for client errors
            except requests.exceptions.ConnectionError as errc:
                logging.error(f"Error Connecting: {errc}")
            except requests.exceptions.Timeout as errt:
                logging.error(f"Timeout Error: {errt}")
            except requests.exceptions.RequestException as err:
                logging.error(f"Other Error: {err}")
            time.sleep(backoff_factor * (2 ** attempt))
        logging.error("Maximum retries exceeded")
        return None

    def fetch_stock_data(self, symbol, resolution, from_time, to_time):
        """Fetch historical stock data in a format suitable for LSTM processing."""
        params = {
            'symbol': symbol,
            'resolution': resolution,
            'from': from_time,
            'to': to_time,
            'token': self.api_key_finnhub
        }
        data = self.fetch_data_with_retry(self.stock_api_url, params)
        if data and 'c' in data:  # Ensure data contains 'close' prices
            # Reformat data for LSTM input (e.g., converting to a DataFrame if not already one)
            return pd.DataFrame(data)
        return data

    def fetch_news(self, query):
        """Fetch news articles."""
        params = {
            'q': query,
            'apiKey': self.api_key_newsapi
        }
        return self.fetch_data_with_retry(self.news_api_url, params)

# Example usage
if __name__ == "__main__":
    fetcher = DataFetcher()
    stock_data = fetcher.fetch_stock_data('AAPL', 'D', 1615299000, 1615385400)
    news_data = fetcher.fetch_news('stock market')
    print(stock_data)
    print(news_data)
