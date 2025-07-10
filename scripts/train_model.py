#!/usr/local/bin/python

# Training Random Forest Classifier based on Titanic Dataset
# This script demonstrates a complete machine learning pipeline:
# 1. Data loading and exploration
# 2. Data preprocessing and cleaning
# 3. Model training and evaluation
# 4. Feature importance analysis

# Import required libraries
import pandas as pd             # For data manipulation and analysis
import numpy as np              # For numerical operations
from sklearn.ensemble import RandomForestClassifier          # Our machine learning model
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report  # Evaluation metrics
import seaborn as sns        # For statistical data visualization
import matplotlib.pyplot as plt  # For plotting graphs
import joblib               # For saving/loading trained model

# STEP 1: DATA LOADING
# Load Kaggle competition datasets
train_data = pd.read_csv('../data/train.csv')  # Training data with survival labels
test_data = pd.read_csv('../data/test.csv')    # Test data for final predictions

# STEP 2: DATA EXPLORATION
# Explore training data to understand its characteristics
train_data.info()      # Shows data types and non-null counts
train_data.describe()  # Statistical summary of numerical columns
train_data.isnull().sum()  # Count missing values in each column

# STEP 3: DATA PREPROCESSING
# Select relevant features for prediction
features = ['Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']

# Preprocess training data
train = train_data[features + ['Survived']].copy()  # Include target variable

# Handle missing values in training data
train['Age'] = train['Age'].fillna(train['Age'].median())  # Fill missing ages with median
train['Embarked'] = train['Embarked'].fillna(train['Embarked'].mode()[0])  # Fill with most common port

# Convert categorical variables to numerical (one-hot encoding)
train = pd.get_dummies(train, columns=['Sex', 'Embarked'], drop_first=True)

# Separate features from target variable
X_train = train.drop('Survived', axis=1)  # Features for training
y_train = train['Survived']               # Target variable (what we predict)

# Preprocess test data (must match training data preprocessing)
test = test_data[features].copy()  # Select same features as training

# Handle missing values using training data statistics (important!)
test['Age'] = test['Age'].fillna(train_data['Age'].median())        # Use original training median
test['Fare'] = test['Fare'].fillna(train_data['Fare'].median())    # Fill missing fare
test['Embarked'] = test['Embarked'].fillna(train_data['Embarked'].mode()[0])  # Use original training mode

# Apply same encoding as training data
test = pd.get_dummies(test, columns=['Sex', 'Embarked'], drop_first=True)

X_test = test  # Test features (no target column in Kaggle competition)

# STEP 4: MODEL TRAINING
# Create and train Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)  # Train on all available training data

# STEP 5: MAKE PREDICTIONS
# Generate predictions for Kaggle test set
predictions = model.predict(X_test)

# STEP 6: ANALYZE FEATURE IMPORTANCE
# Extract and visualize which features matter most
importances = model.feature_importances_
feature_names = X_train.columns
feature_importance_df = pd.DataFrame({
    'Feature': feature_names, 
    'Importance': importances
})
feature_importance_df = feature_importance_df.sort_values(by='Importance', ascending=False)

# Create visualization
sns.barplot(x='Importance', y='Feature', data=feature_importance_df)
plt.title('Feature Importance - Which factors most influence survival?')
plt.show()

# STEP 7: SAVE TRAINED MODEL
# Save model for later use or deployment
joblib.dump(model, 'rf_model_titanic.joblib')
print("Model saved successfully!")

