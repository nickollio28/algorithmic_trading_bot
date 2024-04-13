import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Dropout, concatenate
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import logging

logging.basicConfig(level=logging.INFO)

class StockPricePredictor:
    def __init__(self, dataset_path, news_dataset_path=None, learning_rate=0.001, epochs=100, batch_size=32):
        self.data = pd.read_csv(dataset_path)
        self.news_data = pd.read_csv(news_dataset_path) if news_dataset_path else None
        self.model = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.scaler = StandardScaler()
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.batch_size = batch_size

    def preprocess_data(self):
        """Preprocess data by scaling features and splitting the dataset."""
        if self.news_data is not None:
            # Assume news_data contains 'news_text' for sentiment analysis
            self.data['sentiment'] = self.news_data['news_text'].apply(lambda x: TextBlob(x).sentiment.polarity)
            self.data = pd.merge(self.data, self.news_data[['sentiment']], left_index=True, right_index=True, how='left')
        
        features = self.data.drop(['Stock_Price'], axis=1)
        target = self.data['Stock_Price']
        features_scaled = self.scaler.fit_transform(features)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            features_scaled, target, test_size=0.2, random_state=42
        )

    def build_model(self):
        """Build a neural network using Functional API for predicting stock prices."""
        # Inputs
        main_input = Input(shape=(self.X_train.shape[1],), name='main_input')
        lstm_input = Input(shape=(None, 1), name='lstm_input')

        # Path 1 - Regular feed-forward network
        dense_1 = Dense(128, activation='relu')(main_input)
        dropout_1 = Dropout(0.2)(dense_1)
        dense_2 = Dense(64, activation='relu')(dropout_1)

        # Path 2 - LSTM for sequential data handling
        lstm_layer = LSTM(50)(lstm_input)
        dropout_2 = Dropout(0.2)(lstm_layer)

        # Concatenate both paths
        concatenated = concatenate([dense_2, dropout_2])

        # Output layer
        output = Dense(1)(concatenated)
        
        self.model = Model(inputs=[main_input, lstm_input], outputs=output)
        self.model.compile(optimizer=Adam(learning_rate=self.learning_rate), loss='mean_squared_error')

    def train_model(self):
        """Train the model with early stopping and model checkpointing."""
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        model_checkpoint = ModelCheckpoint('best_model.h5', save_best_only=True)
        
        self.model.fit([self.X_train, self.X_train], self.y_train, epochs=self.epochs, batch_size=self.batch_size, validation_split=0.2, 
                       callbacks=[early_stopping, model_checkpoint])

    def evaluate_model(self):
        """Evaluate the model's performance on the test set."""
        test_loss = self.model.evaluate([self.X_test, self.X_test], self.y_test)
        logging.info(f"Test MSE: {test_loss}")

    def save_model(self):
        """Save the trained model."""
        self.model.save('final_stock_price_model.h5')
        logging.info("Model saved successfully.")

# Usage example
if __name__ == "__main__":
    predictor = StockPricePredictor('path_to_your_dataset.csv', 'path_to_your_news_dataset.csv')
    predictor.preprocess_data()
    predictor.build_model()
    predictor.train_model()
    predictor.evaluate_model()
    predictor.save_model()
