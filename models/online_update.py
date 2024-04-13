import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler

class ModelUpdater:
    def __init__(self, model_path, scaler_path):
        # Load the existing trained model and scaler
        self.model = load_model(model_path)
        self.scaler = StandardScaler()  # Assuming scaler state is saved and loaded appropriately
        self.scaler = self.load_scaler(scaler_path)

    def load_scaler(self, scaler_path):
        """Load the scaler used in the training phase."""
        import joblib
        return joblib.load(scaler_path)

    def preprocess_data(self, new_data):
        """Preprocess new incoming data to be fed into the model for online updates."""
        if isinstance(new_data, dict):  # If data is provided as a dictionary
            new_data = pd.DataFrame([new_data])  # Convert to DataFrame
        elif isinstance(new_data, pd.DataFrame):
            pass  # Use the DataFrame as is
        else:
            raise ValueError("Input data should be a dictionary or a pandas DataFrame.")

        features = new_data.select_dtypes(include=[np.number])  # Selecting numeric columns for scaling
        features_scaled = self.scaler.transform(features)
        return features_scaled

    def update_model(self, new_data, new_labels):
        """Update the model incrementally with new data."""
        preprocessed_data = self.preprocess_data(new_data)
        self.model.fit(preprocessed_data, new_labels, epochs=1, batch_size=len(new_labels))

    def save_updated_model(self, new_model_path):
        """Save the updated model to a new path."""
        self.model.save(new_model_path)
        print("Updated model saved successfully.")

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
    new_labels = np.array([120.5])  # Example new target value

    updater.update_model(new_data, new_labels)
    updater.save_updated_model('path_to_updated_model.h5')
