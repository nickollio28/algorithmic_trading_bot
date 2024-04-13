import pandas as pd
import numpy as np
import logging
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
import joblib

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StockPricePredictor:
    def __init__(self, model_path, scaler_path=None):
        self.model = load_model(model_path)
        if scaler_path:
            self.scaler = joblib.load(scaler_path)  # Load pre-fitted scaler from file if provided
        else:
            self.scaler = StandardScaler()  # Only initialize if no pre-fitted scaler is available

    def preprocess_data(self, data):
        """Preprocess input data in the same way as during training."""
        if isinstance(data, dict):  # If data is provided as a dictionary
            data = pd.DataFrame([data])  # Convert to DataFrame
        elif isinstance(data, pd.DataFrame):
            pass  # Use the DataFrame as is
        else:
            logging.error("Input data should be a dictionary or a pandas DataFrame.")
            raise ValueError("Input data should be a dictionary or a pandas DataFrame.")
        
        # Validate that data includes all necessary features
        expected_features = ['Feature1', 'Feature2', 'Feature3', 'Feature4']  # Add or adjust feature names as needed
        if not all(feature in data.columns for feature in expected_features):
            missing = set(expected_features) - set(data.columns)
            logging.error(f"Missing features in input data: {missing}")
            raise ValueError(f"Missing features: {missing}")
        
        features = data[expected_features]  # Selecting numeric columns for scaling
        features_scaled = self.scaler.transform(features)  # Use transform instead of fit_transform
        return features_scaled.reshape(1, -1), features_scaled.reshape(1, features_scaled.shape[0], 1)  # Prepare for feed-forward and LSTM layers

    def predict(self, input_data):
        """Make predictions using the preprocessed data."""
        try:
            ff_input, lstm_input = self.preprocess_data(input_data)
            predictions = self.model.predict([ff_input, lstm_input])
            return predictions.flatten()  # Flatten to simplify output if needed
        except Exception as e:
            logging.error(f"Prediction error: {e}")
            raise

# Usage example
if __name__ == "__main__":
    predictor = StockPricePredictor('final_stock_price_model.h5', 'scaler.pkl')
    
    # Example new data for prediction
    new_data = {
        'Feature1': 0.5,
        'Feature2': -0.1,
        'Feature3': 3.5,
        'Feature4': 1.2
    }
    
    try:
        predicted_price = predictor.predict(new_data)
        print("Predicted Stock Price:", predicted_price)
    except Exception as e:
        print("Error during prediction:", e)
