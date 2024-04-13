import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RiskManager:
    def __init__(self, max_trade_limit, stop_loss_threshold, volatility_threshold):
        """
        Initializes the RiskManager with specific risk parameters.
        """
        self.set_risk_parameters(max_trade_limit, stop_loss_threshold, volatility_threshold)

    def set_risk_parameters(self, max_trade_limit, stop_loss_threshold, volatility_threshold):
        """
        Validate and set risk management parameters.
        """
        if any(x <= 0 for x in [max_trade_limit, stop_loss_threshold, volatility_threshold]):
            logging.error("Risk parameters must be positive values.")
            raise ValueError("Risk parameters must be positive values.")
        
        self.max_trade_limit = max_trade_limit
        self.stop_loss_threshold = stop_loss_threshold
        self.volatility_threshold = volatility_threshold

    def update_risk_parameters_based_on_market(self, market_conditions):
        """
        Dynamically adjust risk parameters based on current market conditions or predictions.
        """
        self.volatility_threshold = market_conditions.get('new_volatility_threshold', self.volatility_threshold)
        self.stop_loss_threshold = market_conditions.get('new_stop_loss_threshold', self.stop_loss_threshold)
        logging.info("Updated risk parameters based on market conditions.")

    def should_trade(self, current_volatility):
        """
        Determine whether trading conditions are safe based on current market volatility.
        """
        if current_volatility < 0:
            logging.error("Volatility cannot be negative.")
            raise ValueError("Volatility cannot be negative.")

        return current_volatility < self.volatility_threshold

    def calculate_trade_size(self, current_price, available_capital):
        """
        Calculate the size of the trade that does not exceed the max trade limit and considers current market volatility.
        """
        if current_price <= 0 or available_capital <= 0:
            logging.error("Price and capital must be positive values.")
            raise ValueError("Price and capital must be positive values.")

        max_possible_shares = available_capital // current_price
        trade_size = min(max_possible_shares, self.max_trade_limit // current_price)
        return trade_size

    def calculate_stop_loss_price(self, entry_price, market_volatility):
        """
        Calculate the stop loss price for a trade, adjusting for market volatility.
        """
        if entry_price <= 0:
            logging.error("Entry price must be positive.")
            raise ValueError("Entry price must be positive.")

        adjusted_stop_loss_threshold = self.stop_loss_threshold + (market_volatility / 10)
        stop_loss_price = entry_price * (1 - adjusted_stop_loss_threshold)
        return stop_loss_price

# Example usage
if __name__ == "__main__":
    try:
        risk_manager = RiskManager(max_trade_limit=10000, stop_loss_threshold=0.1, volatility_threshold=0.2)
        risk_manager.update_risk_parameters_based_on_market({'new_volatility_threshold': 0.25, 'new_stop_loss_threshold': 0.15})
        print("Should trade:", risk_manager.should_trade(0.15))
        print("Trade size for $150 stock with $5000 capital:", risk_manager.calculate_trade_size(150, 5000))
        print("Stop loss price for $150 entry with market volatility 0.3:", risk_manager.calculate_stop_loss_price(150, 0.3))
    except ValueError as e:
        print(e)
