import pandas as pd
import numpy as np
from keras.models import load_model
from keras.preprocessing.sequence import TimeseriesGenerator
from sklearn.preprocessing import StandardScaler
import joblib
import logging

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelUpdater:
    def __init__(self, model_path, scaler_path):
        # Load the existing trained model and scaler
        self.model = load_model(model_path)
        self.scaler = self.load_scaler(scaler_path)

    def load_scaler(self, scaler_path):
        """Load the scaler used in the training phase."""
        return joblib.load(scaler_path)

    def preprocess_data(self, new_data):
        """Preprocess new incoming data to be fed into the model for online updates."""
        if isinstance(new_data, dict):  # If data is provided as a dictionary
            new_data = pd.DataFrame([new_data])  # Convert to DataFrame
        elif isinstance(new_data, pd.DataFrame):
            pass  # Use the DataFrame as is
        else:
            raise ValueError("Input data should be a dictionary or a pandas DataFrame.")
        
        self.validate_data(new_data)

        features = new_data.select_dtypes(include=[np.number])  # Selecting numeric columns for scaling
        features_scaled = self.scaler.transform(features)
        return features_scaled.reshape(1, features_scaled.shape[0], 1)  # Reshape for LSTM

    def validate_data(self, new_data):
        """Validate new data for expected formats and completeness."""
        required_columns = ['Feature1', 'Feature2', 'Feature3', 'Feature4']
        if not all(col in new_data.columns for col in required_columns):
            missing = list(set(required_columns) - set(new_data.columns))
            logging.error("Missing columns: %s", missing)
            raise ValueError(f"Missing columns: {missing}")

    def update_model(self, new_data, new_labels, batch_size=10):
        """Update the model incrementally with new data in batches."""
        try:
            preprocessed_data = self.preprocess_data(new_data)
            # Assuming new_labels are provided in the same batch structure
            self.model.fit(preprocessed_data, new_labels, epochs=1, batch_size=batch_size)
            logging.info("Model updated successfully.")
        except Exception as e:
            logging.error("Failed to update model: %s", e)
            raise

    def save_updated_model(self, new_model_path):
        """Save the updated model to a new path."""
        self.model.save(new_model_path)
        logging.info("Updated model saved successfully.")

# Usage example
if __name__ == "__main__":
    updater = ModelUpdater('path_to_existing_model.h5', 'path_to_scaler.pkl')
    # Example new data and labels for the update
    new_data = {
        'Feature1': 0.6,
        'Feature2': -0.2,
        'Feature3': 3.7,
        'Feature4': 1.3
    }
    new_labels = np.array([[120.5]])  # Example new target value reshaped for LSTM

    updater.update_model(new_data, new_labels)
    updater.save_updated_model('path_to_updated_model.h5')