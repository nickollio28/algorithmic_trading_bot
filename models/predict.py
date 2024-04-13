import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

class StockPricePredictor:
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.scaler = StandardScaler()

    def preprocess_data(self, data):
        """Preprocess input data in the same way as during training."""
        if isinstance(data, dict):  # If data is provided as a dictionary
            data = pd.DataFrame([data])  # Convert to DataFrame
        elif isinstance(data, pd.DataFrame):
            pass  # Use the DataFrame as is
        else:
            raise ValueError("Input data should be a dictionary or a pandas DataFrame.")
        
        # Assuming 'Stock_Price' column won't be in the prediction data frame
        features = data.select_dtypes(include=[np.number])  # Selecting numeric columns for scaling
        features_scaled = self.scaler.fit_transform(features)
        return features_scaled

    def predict(self, input_data):
        """Make predictions using the preprocessed data."""
        preprocessed_data = self.preprocess_data(input_data)
        predictions = self.model.predict(preprocessed_data)
        return predictions

# Usage example
if __name__ == "__main__":
    # Path to the trained model file
    predictor = StockPricePredictor('final_stock_price_model.h5')
    
    # Example new data for prediction
    new_data = {
        'Feature1': 0.5,
        'Feature2': -0.1,
        'Feature3': 3.5,
        'Feature4': 1.2
    }
    
    predicted_price = predictor.predict(new_data)
    print("Predicted Stock Price:", predicted_price)
