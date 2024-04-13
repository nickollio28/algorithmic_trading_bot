import pandas as pd

class DataCleaner:
    def clean_stock_data(self, data):
        """Convert JSON from Finnhub to pandas DataFrame and clean."""
        df = pd.DataFrame(data['c'], columns=['Close'])
        df['High'] = data['h']
        df['Low'] = data['l']
        df['Open'] = data['o']
        df['Volume'] = data['v']
        df.dropna(inplace=True)
        return df

    def clean_news_data(self, news_data):
        """Extract relevant fields from news data."""
        articles = []
        for article in news_data['articles']:
            articles.append({
                'title': article['title'],
                'description': article['description'],
                'content': article['content']
            })
        return pd.DataFrame(articles)

# Example usage
if __name__ == "__main__":
    cleaner = DataCleaner()
    stock_data = {'c': [100, 101, 102], 'h': [103, 104, 105], 'l': [99, 98, 97], 'o': [100, 101, 102], 'v': [1000, 1010, 1020]}
    news_data = {'articles': [{'title': 'Market up', 'description': 'The market went up today.', 'content': 'More detailed report.'}]}
    cleaned_stock = cleaner.clean_stock_data(stock_data)
    cleaned_news = cleaner.clean_news_data(news_data)
    print(cleaned_stock)
    print(cleaned_news)
