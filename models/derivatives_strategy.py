class DerivativesStrategy:
    def __init__(self, market_data, risk_parameters):
        """
        Initialize with market data and user-defined risk parameters.
        """
        self.market_data = market_data
        self.risk_parameters = risk_parameters

    def futures_trading_strategy(self, position, current_price, target_price, stop_loss):
        """
        A basic futures trading strategy that considers entry and exit points.
        - position: 'long' or 'short'
        - current_price: current market price of the asset
        - target_price: price target to exit the position profitably
        - stop_loss: price level to exit the position to prevent further loss
        """
        if position == 'long':
            if current_price < stop_loss:
                return 'Sell to stop loss', current_price
            elif current_price > target_price:
                return 'Sell to realize profit', current_price
            else:
                return 'Hold', current_price
        elif position == 'short':
            if current_price > stop_loss:
                return 'Buy to stop loss', current_price
            elif current_price < target_price:
                return 'Buy to realize profit', current_price
            else:
                return 'Hold', current_price

    def options_trading_strategy(self, option_type, strike_price, market_volatility):
        """
        Simple options trading strategy that uses market volatility and other parameters to decide.
        - option_type: 'call' or 'put'
        - strike_price: the strike price of the option
        - market_volatility: current market volatility
        """
        if market_volatility > self.risk_parameters['volatility_threshold']:
            if option_type == 'call':
                return 'Buy call', strike_price
            elif option_type == 'put':
                return 'Buy put', strike_price
        else:
            return 'No action', strike_price

    def swap_trading_strategy(self, expected_rate, current_rate):
        """
        Strategy for interest rate swaps based on expectations versus current rates.
        - expected_rate: the rate you expect in the future
        - current_rate: the current market rate
        """
        if expected_rate > current_rate:
            return 'Enter swap to pay fixed, receive floating', current_rate
        elif expected_rate < current_rate:
            return 'Enter swap to pay floating, receive fixed', current_rate
        else:
            return 'No swap action', current_rate

# Example usage
if __name__ == "__main__":
    market_data = {"AAPL": {"current_price": 150, "volatility": 0.3}}
    risk_params = {"volatility_threshold": 0.25}
    strategy = DerivativesStrategy(market_data, risk_params)

    # Futures example
    print(strategy.futures_trading_strategy('long', 150, 160, 145))

    # Options example
    print(strategy.options_trading_strategy('call', 150, market_data["AAPL"]["volatility"]))

    # Swap example
    print(strategy.swap_trading_strategy(1.5, 1.2))
