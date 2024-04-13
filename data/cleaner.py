import pandas as pd
import numpy as np
import re
from scipy import stats

class DataCleaner:
    def clean_stock_data(self, data):
        """Convert JSON from Finnhub to pandas DataFrame, clean, and handle outliers."""
        df = pd.DataFrame(data)
        df.columns = ['Close', 'High', 'Low', 'Open', 'Volume']

        # Impute missing values with forward fill then backward fill as a fallback
        df.fillna(method='ffill', inplace=True)
        df.fillna(method='bfill', inplace=True)

        # Ensure all data is numeric
        df = df[df.applymap(np.isreal).all(1)]

        # Remove outliers using z-score
        df = df[(np.abs(stats.zscore(df.select_dtypes(include=[np.number]))) < 3).all(axis=1)]

        return df

    def clean_news_data(self, news_data):
        """Extract relevant fields from news data and clean text."""
        articles = []
        for article in news_data['articles']:
            clean_title = self.clean_text(article['title'])
            clean_description = self.clean_text(article['description'])
            clean_content = self.clean_text(article['content'])
            articles.append({
                'title': clean_title,
                'description': clean_description,
                'content': clean_content
            })
        return pd.DataFrame(articles)

    def clean_text(self, text):
        """Remove unwanted characters and normalize text."""
        if not text:
            return ""
        text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
        text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
        text = text.lower()  # Convert to lowercase
        return text

# Example usage
if __name__ == "__main__":
    cleaner = DataCleaner()
    stock_data = {'c': [100, 101, None, 103], 'h': [104, 105, 106, None], 'l': [99, 98, 97, 96], 'o': [100, 101, 102, 103], 'v': [1000, 1010, 1020, 1030]}
    news_data = {'articles': [{'title': 'Market Up!', 'description': 'The market went up today...', 'content': 'More detailed report on market rise.'}]}
    cleaned_stock = cleaner.clean_stock_data(stock_data)
    cleaned_news = cleaner.clean_news_data(news_data)
    print(cleaned_stock)
    print(cleaned_news)
