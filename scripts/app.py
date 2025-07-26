#!/usr/local/bin/python

# Flask API for ML Model Serving with Monitoring
# This script creates a REST API to serve machine learning predictions
# with built-in monitoring and metrics collection

# Import required libraries
from flask import Flask, request, jsonify  # Web framework for API
import joblib                              # For loading saved ML models
import pandas as pd                        # For data manipulation
import time                                # For measuring latency

# Prometheus monitoring libraries
from prometheus_client import Counter, Histogram, start_http_server

# --- Initialize app and metrics ---
# STEP 1: CREATE FLASK APPLICATION
app = Flask(__name__)  # Initialize Flask web application

# STEP 2: DEFINE MONITORING METRICS
# Counter: Tracks total number of predictions made
prediction_count = Counter("prediction_total", "Total number of predictions")
# Histogram: Tracks distribution of prediction latencies
latency_histogram = Histogram("prediction_latency_seconds", "Prediction latency in seconds")

# --- Load trained model and columns ---
# STEP 3: LOAD TRAINED MODEL
# Load the pre-trained Random Forest model
model = joblib.load("rf_model_titanic.joblib")
# Load the column names/order used during training (for consistency)
columns = joblib.load("rf_model_titanic_columns.joblib")

# STEP 4: DEFINE API ENDPOINT
@app.route("/predict", methods=["POST"])  # Accept POST requests at /predict
def predict():
    """Handle prediction requests with monitoring"""
    try:
        # Parse JSON input data into pandas DataFrame
        df = pd.DataFrame(request.json)
        
        # MONITORING: Start timing the prediction
        start_time = time.time()
        
        # Make prediction using loaded model
        prediction = model.predict(df)
        
        # MONITORING: Calculate prediction latency
        latency = time.time() - start_time
        
        # UPDATE METRICS
        prediction_count.inc()              # Increment prediction counter
        latency_histogram.observe(latency)  # Record latency measurement
        
        # Return prediction as JSON response
        return jsonify({"prediction": int(prediction[0])})
        
    except Exception as e:
        # Handle errors gracefully and return error message
        return jsonify({"error": str(e)}), 400  # HTTP 400 Bad Request

# STEP 5: START THE APPLICATION
if __name__ == "__main__":
    # Start Prometheus metrics server on port 8001
    # This exposes /metrics endpoint for monitoring tools
    start_http_server(8001)
    
    # Start Flask API server on port 8000
    # host="0.0.0.0" makes it accessible from outside the container
    app.run(host="0.0.0.0", port=8000)
    
    # USAGE EXAMPLE:
    # curl -X POST http://localhost:8000/predict \
    #   -H "Content-Type: application/json" \
    #   -d '{"Pclass": 3, "Sex_male": 1, "Age": 22, "SibSp": 1, "Parch": 0, "Fare": 7.25, "Embarked_Q": 0, "Embarked_S": 1}'
    #
    # MONITORING:
    # curl http://localhost:8001/metrics  # View Prometheus metrics
