import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DerivativesStrategy:
    def __init__(self, market_data, risk_parameters, model_predictions=None):
        """
        Initialize with market data, user-defined risk parameters, and model predictions.
        """
        self.market_data = market_data
        self.risk_parameters = risk_parameters
        self.model_predictions = model_predictions
        self.validate_parameters()

    def validate_parameters(self):
        """
        Validates the necessary parameters to ensure they meet expected criteria.
        """
        if not isinstance(self.market_data, dict) or not isinstance(self.risk_parameters, dict):
            logging.error("Market data and risk parameters should be dictionaries.")
            raise ValueError("Market data and risk parameters should be dictionaries.")

        required_params = ['volatility_threshold', 'profit_target', 'stop_loss_limit']
        for param in required_params:
            if param not in self.risk_parameters:
                logging.error(f"{param} missing in risk parameters.")
                raise KeyError(f"{param} missing in risk parameters.")

    def futures_trading_strategy(self, position, current_price):
        """
        Advanced futures trading strategy that considers predictive model outputs.
        """
        target_price = self.model_predictions.get('target_price')
        stop_loss = self.model_predictions.get('stop_loss')

        try:
            if position not in ['long', 'short']:
                raise ValueError("Position must be either 'long' or 'short'.")

            if current_price < stop_loss and position == 'long':
                return 'Sell to stop loss', current_price
            elif current_price > target_price and position == 'long':
                return 'Sell to realize profit', current_price
            elif current_price > stop_loss and position == 'short':
                return 'Buy to stop loss', current_price
            elif current_price < target_price and position == 'short':
                return 'Buy to realize profit', current_price
            else:
                return 'Hold', current_price
        except Exception as e:
            logging.error(f"Error in futures strategy: {e}")
            raise

    def options_trading_strategy(self, option_type, strike_price):
        """
        Enhanced options trading strategy using volatility forecasts.
        """
        market_volatility = self.market_data.get('volatility', 0)

        try:
            if option_type not in ['call', 'put']:
                raise ValueError("Option type must be either 'call' or 'put'.")

            if market_volatility > self.risk_parameters['volatility_threshold']:
                action = 'Buy call' if option_type == 'call' else 'Buy put'
                return action, strike_price
            else:
                return 'No action', strike_price
        except Exception as e:
            logging.error(f"Error in options strategy: {e}")
            raise

    def swap_trading_strategy(self, expected_rate, current_rate):
        """
        Strategy for interest rate swaps.
        """
        try:
            if expected_rate > current_rate:
                return 'Enter swap to pay fixed, receive floating', current_rate
            elif expected_rate < current_rate:
                return 'Enter swap to pay floating, receive fixed', current_rate
            else:
                return 'No swap action', current_rate
        except Exception as e:
            logging.error(f"Error in swap strategy: {e}")
            raise

# Example usage
if __name__ == "__main__":
    market_data = {"AAPL": {"current_price": 150, "volatility": 0.3}}
    risk_params = {"volatility_threshold": 0.25, "profit_target": 160, "stop_loss_limit": 145}
    model_predictions = {"target_price": 160, "stop_loss": 145}
    strategy = DerivativesStrategy(market_data, risk_params, model_predictions)

    print(strategy.futures_trading_strategy('long', market_data["AAPL"]["current_price"]))
    print(strategy.options_trading_strategy('call', 150))
    print(strategy.swap_trading_strategy(1.5, 1.2))
