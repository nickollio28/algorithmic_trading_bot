import requests

class DataFetcher:
    def __init__(self):
        self.stock_api_url = 'https://finnhub.io/api/v1/stock/candle'
        self.news_api_url = 'https://newsapi.org/v2/everything'
        self.api_key_finnhub = 'YOUR_FINNHUB_API_KEY'
        self.api_key_newsapi = 'YOUR_NEWSAPI_KEY'

    def fetch_stock_data(self, symbol, resolution, from_time, to_time):
        """Fetch historical stock data."""
        params = {
            'symbol': symbol,
            'resolution': resolution,
            'from': from_time,
            'to': to_time,
            'token': self.api_key_finnhub
        }
        response = requests.get(self.stock_api_url, params=params)
        return response.json()

    def fetch_news(self, query):
        """Fetch news articles."""
        params = {
            'q': query,
            'apiKey': self.api_key_newsapi
        }
        response = requests.get(self.news_api_url, params=params)
        return response.json()
    
    def fetch_available_capital():
        """Fetch total amount I am investing"""
        # TODO: update
        return 1000

# Example usage
if __name__ == "__main__":
    fetcher = DataFetcher()
    stock_data = fetcher.fetch_stock_data('AAPL', 'D', 1615299000, 1615385400)
    news_data = fetcher.fetch_news('stock market')
    print(stock_data)
    print(news_data)
