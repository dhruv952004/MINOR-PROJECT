import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

# Create saved_models directory if it doesn't exist
os.makedirs('Model/saved_models', exist_ok=True)

# Initialize models
diabetes_model = DecisionTreeClassifier(random_state=42)
heart_model = DecisionTreeClassifier(random_state=42)
parkinsons_model = DecisionTreeClassifier(random_state=42)

# Save dummy models for now (we'll train them properly once we have the correct datasets)
pickle.dump(diabetes_model, open('Model/saved_models/diabetes_model.sav', 'wb'))
pickle.dump(heart_model, open('Model/saved_models/heart_disease_model.sav', 'wb'))
pickle.dump(parkinsons_model, open('Model/saved_models/parkinsons_model.sav', 'wb'))

print("Models saved successfully! Note: These are placeholder models until proper training data is available.") 