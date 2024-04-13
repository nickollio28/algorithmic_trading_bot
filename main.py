# Import necessary modules and classes
from fetcher import DataFetcher
from cleaner import DataCleaner
from processor import DataProcessor
from trainer import ModelTrainer
from strategy import TradingStrategy
from executer import TradeExecuter
from risk_management import RiskManager
from config import Config
import time

# Initialize components
fetcher = DataFetcher()
cleaner = DataCleaner()
processor = DataProcessor()
trainer = ModelTrainer()
executer = TradeExecuter(Config.TRADE_EXECUTION_URL, Config.API_KEY_BROKERAGE)
risk_manager = RiskManager(Config.MAX_TRADE_LIMIT, Config.STOP_LOSS_THRESHOLD, Config.VOLATILITY_THRESHOLD)

# Define main trading loop
def main_trading_loop():
    while True:
        try:
            # Fetch data from sources
            raw_data = fetcher.fetch_data()
            
            # Clean and process the data
            cleaned_data = cleaner.clean_data(raw_data)
            processed_data = processor.process_data(cleaned_data)

            # Train the model
            trainer.train_model(processed_data)

            # Get market data for trading decision
            market_data = processed_data[-1]  # Example: Last processed data point

            # Implement trading strategy
            strategy = TradingStrategy(trainer.model, risk_manager)
            action, price = strategy.decide(market_data)

            # Execute trade
            if action != 'Hold':
                trade_size = risk_manager.calculate_trade_size(price, available_capital)
                executer.execute_trade(action.lower(), market_data['symbol'], trade_size, price)
                risk_manager.check_order_status(order_id)  # Assuming order_id is returned by execute_trade

            time.sleep(60)  # Sleep for 1 minute before next iteration
        except Exception as e:
            print("Error occurred:", str(e))
            time.sleep(60)  # Sleep for 1 minute and continue loop

# Entry point of the program
if __name__ == "__main__":
    main_trading_loop()
