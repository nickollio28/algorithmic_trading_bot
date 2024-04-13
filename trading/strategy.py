import logging

class TradingStrategy:
    def __init__(self, model, risk_manager):
        self.model = model
        self.risk_manager = risk_manager

    def decide(self, market_data):
        logging.info("Evaluating market data for trading decision.")
        
        # Extract and use technical indicators from the market data
        indicators = market_data[['SMA_20', 'SMA_50', 'EMA_20', 'EMA_50', 'RSI', 'Upper_Band', 'Lower_Band']]
        current_price = market_data['current_price']
        volume = market_data['volume']

        # Decision logic based on moving averages crossover
        if indicators['SMA_20'].iloc[-1] > indicators['SMA_50'].iloc[-1]:
            action = 'Buy'
        elif indicators['SMA_20'].iloc[-1] < indicators['SMA_50'].iloc[-1]:
            action = 'Sell'
        else:
            action = 'Hold'

        # Additional logic using RSI for overbought/oversold
        if indicators['RSI'].iloc[-1] > 70:
            action = 'Sell'  # Overbought
        elif indicators['RSI'].iloc[-1] < 30:
            action = 'Buy'  # Oversold

        # Check Bollinger Bands
        if current_price > indicators['Upper_Band'].iloc[-1]:
            action = 'Sell'  # Price is high
        elif current_price < indicators['Lower_Band'].iloc[-1]:
            action = 'Buy'  # Price is low

        # Apply risk management
        trade_size = self.risk_manager.calculate_trade_size(current_price, volume)
        logging.info(f"Action: {action}, Trade Size: {trade_size}")

        return action, trade_size

# Example usage
if __name__ == "__main__":
    from models.model import TradingModel
    from risk_management import RiskManager
    
    # Assuming model and risk_manager are defined elsewhere
    model = TradingModel()
    risk_manager = RiskManager(max_trade_limit=100000, stop_loss_threshold=0.1, volatility_threshold=0.2)
    strategy = TradingStrategy(model, risk_manager)
    
    # Dummy market data
    market_data = {
        'SMA_20': [120, 118, 117],
        'SMA_50': [115, 114, 113],
        'EMA_20': [119, 117, 116],
        'EMA_50': [114, 113, 112],
        'RSI': [75, 60, 25],
        'Upper_Band': [130, 128, 126],
        'Lower_Band': [110, 108, 106],
        'current_price': 107,
        'volume': 5000
    }
    action, trade_size = strategy.decide(market_data)
    print(f"Decided Action: {action}, Trade Size: {trade_size}")
