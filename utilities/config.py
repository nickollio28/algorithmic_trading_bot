# config.py
class Config:
    API_KEY_FINNHUB = 'your_finnhub_api_key'
    API_KEY_NEWSAPI = 'your_newsapi_key'
    DATABASE_URI = 'your_database_uri'

    # Risk management parameters
    MAX_TRADE_LIMIT = 10000
    STOP_LOSS_THRESHOLD = 0.1
    VOLATILITY_THRESHOLD = 0.2

    # Other configurable parameters
    TRADE_EXECUTION_URL = 'https://api.brokerage.com/orders'

# Example usage:
if __name__ == "__main__":
    print("API Key for Finnhub:", Config.API_KEY_FINNHUB)
