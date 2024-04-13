import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class OptionsStrategy:
    def __init__(self, stock_price, strike_price, premium, current_volatility, risk_appetite, model_forecasts=None):
        # Input validations
        self.validate_inputs(stock_price, strike_price, premium, current_volatility, risk_appetite)

        self.stock_price = stock_price
        self.strike_price = strike_price
        self.premium = premium
        self.current_volatility = current_volatility
        self.risk_appetite = risk_appetite  # Scale of 0-1, where 1 is very aggressive.
        self.model_forecasts = model_forecasts  # This should include predicted price and volatility

    def validate_inputs(self, stock_price, strike_price, premium, current_volatility, risk_appetite):
        if not all(isinstance(x, (int, float)) for x in [stock_price, strike_price, premium, current_volatility, risk_appetite]):
            logging.error("All inputs must be numbers.")
            raise ValueError("All inputs must be numbers.")
        if not (0 <= risk_appetite <= 1):
            logging.error("Risk appetite must be between 0 and 1.")
            raise ValueError("Risk appetite must be between 0 and 1.")

    def covered_call(self):
        """
        Implement a covered call strategy:
        - Sell call options on stocks you already own.
        - Suitable when expecting the stock price to rise moderately or remain stable.
        """
        try:
            if self.model_forecasts and self.model_forecasts.get('price_upside') < self.risk_appetite:
                if self.stock_price <= self.strike_price and self.current_volatility > 0.2:
                    income = self.premium * 100  # Assuming 1 option contract covers 100 shares.
                    logging.info(f"Sell a covered call to earn an income of {income}.")
                    return "Sell Covered Call", income
            return "No Action", 0
        except Exception as e:
            logging.error("Error in covered call strategy: %s", e)
            raise

    def protective_put(self):
        """
        Implement a protective put strategy:
        - Buy put options to protect against a decline in stock price.
        - Suitable when you own the stock and are worried about potential downsides.
        """
        try:
            if self.model_forecasts and self.model_forecasts.get('price_downside') > self.risk_appetite:
                if self.stock_price >= self.strike_price and self.current_volatility > 0.3:
                    cost = self.premium * 100  # Assuming 1 option contract covers 100 shares.
                    logging.info(f"Buy a protective put to hedge against price drop at a cost of {cost}.")
                    return "Buy Protective Put", -cost
            return "No Action", 0
        except Exception as e:
            logging.error("Error in protective put strategy: %s", e)
            raise

# Example usage
if __name__ == "__main__":
    model_forecasts = {'price_upside': 0.4, 'price_downside': 0.6}
    try:
        strategy = OptionsStrategy(stock_price=150, strike_price=155, premium=2, current_volatility=0.25, risk_appetite=0.5, model_forecasts=model_forecasts)
        action, value = strategy.covered_call()
        print(action, value)

        action, value = strategy.protective_put()
        print(action, value)
    except Exception as e:
        logging.error("Failed to execute strategies: %s", e)
