import pandas as pd
import numpy as np

class DataProcessor:
    def add_technical_indicators(self, df, indicators=['SMA', 'EMA', 'RSI', 'Bollinger']):
        if 'Close' not in df.columns:
            raise ValueError("DataFrame must contain 'Close' column")

        # Ensure the DataFrame is long enough for the largest window size
        if len(df) < 50:
            raise ValueError("DataFrame must have at least 50 rows to calculate all indicators")

        if 'SMA' in indicators:
            # Simple Moving Averages
            df['SMA_20'] = df['Close'].rolling(window=20).mean()
            df['SMA_50'] = df['Close'].rolling(window=50).mean()

        if 'EMA' in indicators:
            # Exponential Moving Averages
            df['EMA_20'] = df['Close'].ewm(span=20, adjust=False).mean()
            df['EMA_50'] = df['Close'].ewm(span=50, adjust=False).mean()

        if 'RSI' in indicators:
            # Relative Strength Index (RSI)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).fillna(0)
            loss = (-delta.where(delta < 0, 0)).fillna(0)
            avg_gain = gain.rolling(window=14).mean()
            avg_loss = loss.rolling(window=14).mean()
            rs = avg_gain / avg_loss
            df['RSI'] = 100 - (100 / (1 + rs))

        if 'Bollinger' in indicators:
            # Bollinger Bands
            df['Middle_Band'] = df['Close'].rolling(window=20).mean()
            df['STD'] = df['Close'].rolling(window=20).std()
            df['Upper_Band'] = df['Middle_Band'] + (df['STD'] * 2)
            df['Lower_Band'] = df['Middle_Band'] - (df['STD'] * 2)

        # Normalize technical indicators to ensure they are on the same scale
        df = self.normalize_features(df, ['SMA_20', 'SMA_50', 'EMA_20', 'EMA_50', 'RSI', 'Upper_Band', 'Middle_Band', 'Lower_Band'])

        return df

    def normalize_features(self, df, feature_names):
        """Normalize selected features within the DataFrame."""
        for feature in feature_names:
            df[feature] = (df[feature] - df[feature].mean()) / df[feature].std()
        return df

# Example usage
if __name__ == "__main__":
    processor = DataProcessor()
    stock_data = {'Close': [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120]}
    df = pd.DataFrame(stock_data)
    try:
        processed_data = processor.add_technical_indicators(df)
        print(processed_data)
    except ValueError as e:
        print(e)
