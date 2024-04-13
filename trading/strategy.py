import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TradingStrategy:
    def __init__(self, model, risk_parameters):
        """
        Initialize with a trained model and risk management parameters.
        """
        self.model = model
        self.validate_risk_parameters(risk_parameters)
        self.risk_parameters = risk_parameters

    def validate_risk_parameters(self, params):
        """
        Validate risk management parameters to ensure they meet expected criteria.
        """
        required_keys = ['profit_target', 'stop_loss', 'volume_threshold', 'volatility_threshold']
        for key in required_keys:
            if key not in params:
                logging.error(f"Missing risk parameter: {key}")
                raise KeyError(f"Missing risk parameter: {key}")
            if not isinstance(params[key], (int, float)) or params[key] < 0:
                logging.error(f"Invalid value for {key}: {params[key]}")
                raise ValueError(f"Invalid value for {key}: {params[key]}")

    def decide(self, market_data):
        """
        Make a trading decision based on model output and market data.
        """
        try:
            prediction = self.model.predict(market_data)
            current_price = market_data['current_price']
            predicted_price = prediction['predicted_price']
            market_volatility = market_data.get('volatility', 0)

            if market_volatility < self.risk_parameters['volatility_threshold'] and \
               predicted_price > current_price * (1 + self.risk_parameters['profit_target']):
                if market_data['volume'] > self.risk_parameters['volume_threshold']:
                    return 'Buy', predicted_price
            elif predicted_price < current_price * (1 - self.risk_parameters['stop_loss']):
                return 'Sell', predicted_price
            return 'Hold', current_price
        except KeyError as e:
            logging.error(f"Missing data for decision making: {e}")
            raise
        except Exception as e:
            logging.error(f"Error during decision making: {e}")
            raise

    def adjust_positions(self, portfolio):
        """
        Adjust existing positions based on updated market conditions or internal risk assessments.
        """
        try:
            for stock, details in portfolio.items():
                if details['position'] == 'long' and details['price'] < self.risk_parameters['stop_loss_price']:
                    return 'Sell', stock
                elif details['position'] == 'short' and details['price'] > self.risk_parameters['profit_target_price']:
                    return 'Buy to cover', stock
            return 'Hold all', None
        except KeyError as e:
            logging.error(f"Invalid portfolio data: {e}")
            raise
        except Exception as e:
            logging.error(f"Error adjusting positions: {e}")
            raise

# Usage example
if __name__ == "__main__":
    from model import Model  # Assuming you have a Model class that can predict market movements -- have to save model in train.py, and import it as .h5 file
    model = Model()
    risk_params = {'profit_target': 0.05, 'stop_loss': 0.05, 'volume_threshold': 10000, 'volatility_threshold': 0.2}
    strategy = TradingStrategy(model, risk_params)

    market_data = {'current_price': 100, 'predicted_price': 105, 'volume': 12000, 'volatility': 0.15}
    action, price = strategy.decide(market_data)
    print(action, price)

    portfolio = {'AAPL': {'position': 'long', 'price': 95}}
    adjustment = strategy.adjust_positions(portfolio)
    print(adjustment)
