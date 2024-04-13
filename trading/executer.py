import requests
import logging
import asyncio
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TradeExecuter:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.api_key = api_key

    async def execute_trade(self, action, symbol, quantity, price=None):
        """
        Asynchronously send a trade order to the brokerage API to improve execution speed.
        """
        if action not in ['buy', 'sell']:
            logging.error("Invalid action specified. Must be 'buy' or 'sell'.")
            raise ValueError("Action must be 'buy' or 'sell'.")

        data = {
            'action': action,
            'symbol': symbol,
            'quantity': quantity,
            'price': price,
            'apikey': self.api_key
        }
        headers = {'Content-Type': 'application/json'}
        
        try:
            async with requests.AsyncClient() as client:
                response = await client.post(f"{self.api_url}/orders", json=data, headers=headers)
                response.raise_for_status()  # Raises HTTPError for bad responses
                logging.info(f"Trade executed: {action} {quantity} shares of {symbol} at {price}")
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")

    async def check_order_status(self, order_id):
        """
        Asynchronously check the status of an order.
        """
        try:
            async with requests.AsyncClient() as client:
                response = await client.get(f"{self.api_url}/orders/{order_id}", params={'apikey': self.api_key})
                response.raise_for_status()  # Raises HTTPError for bad responses
                logging.info(f"Order status: {json.loads(response.text)['status']}")
        except requests.exceptions.HTTPError as err:
            logging.error(f"HTTP error occurred: {err}")
        except Exception as err:
            logging.error(f"An error occurred: {err}")

# Example usage
if __name__ == "__main__":
    executer = TradeExecuter("https://api.brokerage.com", "your_api_key")
    try:
        # Example executing a buy order
        asyncio.run(executer.execute_trade('buy', 'AAPL', 10, price=150.50))
        # Example checking an order status
        asyncio.run(executer.check_order_status("123456"))
    except Exception as e:
        logging.error(f"An exception occurred: {e}")
