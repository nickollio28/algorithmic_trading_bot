import requests
import os
import time
import logging
import pandas as pd

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class DataFetcher:
    def __init__(self):
        self.stock_api_url = 'https://finnhub.io/api/v1/stock/candle'
        self.news_api_url = 'https://newsapi.org/v2/everything'
        self.api_key_finnhub = os.getenv('FINNHUB_API_KEY')
        self.api_key_newsapi = os.getenv('NEWSAPI_KEY')
    
    def fetch_data_with_retry(self, url, params):
        """Fetch data with retries and exponential backoff."""
        retry_strategy = Retry(
            total=5,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS"],
            backoff_factor=1
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session = requests.Session()
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        try:
            response = session.get(url, params=params)
            response.raise_for_status()  # Will raise an HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Fetching data failed: %s", e)
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
            return pd.DataFrame(data)
        return None

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
