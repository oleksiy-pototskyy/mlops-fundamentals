#!/bin/bash

# API Testing Script for ML Model
# This script generates random passenger data and sends prediction requests
# to test the Flask API endpoint with realistic Titanic dataset values

# COMMAND LINE ARGUMENT HANDLING
# Use first argument as number of requests, default to 1 if not provided
# Usage: ./predict_random.sh 5  (sends 5 requests)
NUM_REQUESTS=${1:-1}

echo "Sending $NUM_REQUESTS prediction request(s) to /predict endpoint"
echo ""

# MAIN LOOP: Generate and send multiple requests
for ((i=1; i<=NUM_REQUESTS; i++))
do
  # STEP 1: GENERATE RANDOM FEATURE VALUES
  # Generate realistic values based on Titanic dataset ranges
  
  PCLASS=$(( (RANDOM % 3) + 1 ))                            # Passenger class: 1, 2, or 3
  AGE=$(awk -v min=1 -v max=80 'BEGIN{srand(); print int(min+rand()*(max-min+1))}')  # Age: 1-80 years
  SIBSP=$(( RANDOM % 4 ))                                   # Siblings/spouses: 0-3
  PARCH=$(( RANDOM % 3 ))                                   # Parents/children: 0-2
  FARE=$(awk -v min=5 -v max=100 'BEGIN{srand(); printf "%.2f", min+rand()*(max-min)}')  # Ticket fare: $5-100

  # STEP 2: ENCODE CATEGORICAL VARIABLES
  # These must match the one-hot encoding used during model training
  
  # Gender encoding (binary): 1 = male, 0 = female
  SEX_MALE=$(( RANDOM % 2 ))

  # Port of embarkation encoding (one-hot with drop_first=True)
  # Original ports: C=Cherbourg, Q=Queenstown, S=Southampton
  # After drop_first: only Q and S columns remain (C is implicit when both are 0)
  EMBARKED_Q=$(( RANDOM % 2 ))
  if [ "$EMBARKED_Q" -eq 1 ]; then
    EMBARKED_S=0  # If Q=1, then S=0 (passenger embarked at Queenstown)
  else
    EMBARKED_S=1  # If Q=0, then S=1 (passenger embarked at Southampton)
  fi
  # Note: C (Cherbourg) is represented by Q=0, S=0

  # STEP 3: BUILD JSON PAYLOAD
  # Create JSON array with single passenger record
  # Column names must exactly match training data after preprocessing
  read -r -d '' PAYLOAD <<EOF
[{
  "Pclass": $PCLASS,
  "Age": $AGE,
  "SibSp": $SIBSP,
  "Parch": $PARCH,
  "Fare": $FARE,
  "Sex_male": $SEX_MALE,
  "Embarked_Q": $EMBARKED_Q,
  "Embarked_S": $EMBARKED_S
}]
EOF

  # STEP 4: DISPLAY INPUT DATA
  echo "Request $i:"
  echo "$PAYLOAD"

  # STEP 5: SEND HTTP REQUEST TO API
  # Use curl to send POST request to Flask API endpoint
  RESPONSE=$(curl -s -X POST http://localhost:8000/predict \
       -H "Content-Type: application/json" \
       -d "$PAYLOAD")
  # -s: silent mode (no progress bar)
  # -X POST: HTTP POST method
  # -H: set Content-Type header
  # -d: send JSON data in request body

  # STEP 6: DISPLAY PREDICTION RESULT
  echo "Prediction: $RESPONSE"
  echo "----------------------------------------"
done

# USAGE EXAMPLES:
# ./predict_random.sh        # Send 1 request
# ./predict_random.sh 10     # Send 10 requests
# ./predict_random.sh 100    # Load test with 100 requests
#
# EXPECTED OUTPUT:
# {"prediction": 0}  # 0 = did not survive
# {"prediction": 1}  # 1 = survived
