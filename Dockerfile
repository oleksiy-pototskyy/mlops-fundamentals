# Use official Python base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY scripts/ scripts/
COPY data/ data/

# Run the training script
# Change working directory to scripts/ and run the Python script
WORKDIR /app/scripts
CMD ["python", "train_model.py"]
