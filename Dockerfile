# Use official Python base image
FROM python:3.13.5-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY scripts/ scripts/
COPY data/ data/

# Run the training script
CMD ["python", "scripts/train_model.py"]
