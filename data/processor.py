class DataProcessor:
    def add_technical_indicators(self, df):
        """Add technical indicators to the DataFrame."""
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        return df

# Example usage
if __name__ == "__main__":
    processor = DataProcessor()
    stock_data = {'Close': [100, 101, 102, 103, 104, 105]}
    df = pd.DataFrame(stock_data)
    processed_data = processor.add_technical_indicators(df)
    print(processed_data)
