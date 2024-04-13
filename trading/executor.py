import requests

class TradeExecuter:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    def execute_trade(self, action, symbol, quantity, price=None):
        """
        Send a trade order to the brokerage API.
        - action: 'buy' or 'sell'
        - symbol: Stock symbol
        - quantity: Number of shares
        - price: Optional price for limit orders
        """
        data = {
            'action': action,
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'apikey': self.api_key
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(f"{self.api_url}/orders", json=data, headers=headers)
        if response.status_code == 200:
            print(f"Trade executed: {action} {quantity} shares of {symbol} at {price}")
        else:
            print(f"Failed to execute trade: {response.text}")

    def check_order_status(self, order_id):
        """
        Check the status of an order.
        """
        response = requests.get(f"{self.api_url}/orders/{order_id}", params={'apikey': self.api_key})
        if response.status_code == 200:
            print(f"Order status: {response.json()['status']}")
        else:
            print(f"Failed to check order status: {response.text}")

# Example usage
if __name__ == "__main__":
    executer = TradeExecuter("https://api.brokerage.com", "your_api_key")
    # Example executing a buy order
    executer.execute_trade('buy', 'AAPL', 10, price=150.50)
    # Example checking an order status
    executer.check_order_status("123456")
