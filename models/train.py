import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint

class StockPricePredictor:
    def __init__(self, dataset_path):
        self.data = pd.read_csv(dataset_path)
        self.model = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None
        self.scaler = StandardScaler()

    def preprocess_data(self):
        """Preprocess data by scaling features and splitting the dataset."""
        features = self.data.drop(['Stock_Price'], axis=1)
        target = self.data['Stock_Price']
        features_scaled = self.scaler.fit_transform(features)

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            features_scaled, target, test_size=0.2, random_state=42
        )

    def build_model(self):
        """Build a neural network for predicting stock prices."""
        self.model = Sequential([
            Dense(128, activation='relu', input_dim=self.X_train.shape[1]),
            Dropout(0.2),
            Dense(64, activation='relu'),
            Dense(1)
        ])
        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')

    def train_model(self):
        """Train the model with early stopping and model checkpointing."""
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
        model_checkpoint = ModelCheckpoint('best_model.h5', save_best_only=True)
        
        self.model.fit(self.X_train, self.y_train, epochs=100, batch_size=32, validation_split=0.2, 
                       callbacks=[early_stopping, model_checkpoint])

    def evaluate_model(self):
        """Evaluate the model's performance on the test set."""
        test_loss = self.model.evaluate(self.X_test, self.y_test)
        print(f"Test MSE: {test_loss}")

    def save_model(self):
        """Save the trained model."""
        self.model.save('final_stock_price_model.h5')
        print("Model saved successfully.")

# Usage example
if __name__ == "__main__":
    predictor = StockPricePredictor('path_to_your_dataset.csv')
    predictor.preprocess_data()
    predictor.build_model()
    predictor.train_model()
    predictor.evaluate_model()
    predictor.save_model()
