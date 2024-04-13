import logging
import time
from data.fetcher import DataFetcher
from data.cleaner import DataCleaner
from data.processor import DataProcessor
from models.train import ModelTrainer
from trading.strategy import TradingStrategy
from trading.executer import TradeExecuter
from trading.risk_management import RiskManager
from utilities.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize components
fetcher = DataFetcher()
cleaner = DataCleaner()
processor = DataProcessor()
trainer = ModelTrainer()
executer = TradeExecuter(Config.TRADE_EXECUTION_URL, Config.API_KEY_BROKERAGE)
risk_manager = RiskManager(Config.MAX_TRADE_LIMIT, Config.STOP_LOSS_THRESHOLD, Config.VOLATILITY_THRESHOLD)

def main_trading_loop():
    stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'FB', 'TSLA']  # Example list of stocks
    while True:
        for symbol in stocks:
            try:
                # Fetch and process data for each stock
                raw_data = fetcher.fetch_stock_data(symbol, '1d')  # Fetch daily data for the stock
                cleaned_data = cleaner.clean_stock_data(raw_data)
                processed_data = processor.add_technical_indicators(cleaned_data)
                logging.info(f"Data cleaned and processed for {symbol}.")

                # Update model with new data or retrain if necessary
                model = trainer.update_model(processed_data)  # Assuming we have a method to update or retrain

                # Get market data for trading decision
                market_data = {'current_price': processed_data['Close'].iloc[-1], 'volume': processed_data['Volume'].iloc[-1]}

                # Implement trading strategy
                strategy = TradingStrategy(model, risk_manager)
                action, trade_size = strategy.decide(market_data)
                logging.info(f"Trading decision for {symbol}: {action} at price {market_data['current_price']}")

                # Execute trade
                if action != 'Hold':
                    order_id = executer.execute_trade(action.lower(), symbol, trade_size, market_data['current_price'])
                    order_status = executer.check_order_status(order_id)
                    logging.info(f"Trade executed for {symbol}. Order ID: {order_id}, Status: {order_status}")

            except Exception as e:
                logging.error(f"Error occurred for {symbol}: {str(e)}")
        time.sleep(60)  # Sleep for 1 minute before next iteration

if __name__ == "__main__":
    main_trading_loop()
