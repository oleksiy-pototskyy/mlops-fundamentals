# MLOps Fundamentals - Titanic Survival Prediction

A comprehensive machine learning project demonstrating MLOps practices using the Titanic dataset. This project covers the complete ML pipeline from data preprocessing to model deployment using modern DevOps tools.

## 📁 Project Structure

```
mlops-fundamentals/
├── data/                           # Dataset files
│   ├── train.csv                   # Training data with survival labels
│   └── test.csv                    # Test data for predictions
├── scripts/                        # Python scripts
│   └── train_model.py             # Main ML training pipeline
├── .github/workflows/             # GitHub Actions CI/CD
│   └── ci.yml                     # Automated testing and training
├── Dockerfile                     # Container configuration
├── titanic-train-job.yaml        # Kubernetes Job definition
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Docker (optional)
- Kubernetes cluster (optional)

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd mlops-fundamentals

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Training Pipeline

```bash
# Execute the ML training script
cd scripts
python train_model.py
```

## 📊 Machine Learning Pipeline

The `train_model.py` script demonstrates a complete ML workflow:

1. **Data Loading** - Load Titanic train/test datasets
2. **Data Exploration** - Analyze data structure and missing values
3. **Data Preprocessing** - Handle missing values and encode categorical features
4. **Model Training** - Train Random Forest classifier
5. **Predictions** - Generate predictions for test set
6. **Feature Analysis** - Visualize feature importance
7. **Model Persistence** - Save trained model

### Key Learning Concepts
- Data leakage prevention
- Proper train/test preprocessing
- Feature engineering with one-hot encoding
- Model evaluation and interpretation

## 🐳 Docker Usage

### Build Docker Image
```bash
# Build the training container
docker build -t titanic-train .
```

### Run Training in Container
```bash
# Execute training pipeline in Docker
docker run titanic-train
```

### Docker Architecture
- **Base Image**: `python:3.10-slim`
- **Working Directory**: `/app/scripts`
- **Dependencies**: Installed from `requirements.txt`
- **Execution**: Runs `train_model.py` from scripts directory

## ☸️ Kubernetes Deployment

### Deploy Training Job
```bash
# Apply Kubernetes Job configuration
kubectl apply -f titanic-train-job.yaml
```

### Monitor Job Execution
```bash
# Check job status
kubectl get jobs

# View job logs
kubectl logs job/titanic-train-job

# Describe job details
kubectl describe job titanic-train-job
```

### Job Configuration Features
- **Resource Limits**: 1GB RAM, 1 CPU core maximum
- **Resource Requests**: 512MB RAM, 0.5 CPU core minimum
- **Retry Policy**: Maximum 2 retries on failure
- **Auto-cleanup**: Job deleted after 1 hour completion

## 🔄 CI/CD Pipeline

GitHub Actions automatically:
- Triggers on push/PR to main branch
- Sets up Python 3.13.5 environment
- Installs project dependencies
- Executes training pipeline
- Reports success/failure status

### Workflow File: `.github/workflows/ci.yml`

## 📋 Dependencies

| Package | Purpose |
|---------|----------|
| pandas | Data manipulation and analysis |
| numpy | Numerical operations |
| scikit-learn | Machine learning algorithms |
| seaborn | Statistical data visualization |
| matplotlib | Plotting and charts |
| joblib | Model serialization |

## 🛠️ Development Commands

### Local Development
```bash
# Install in development mode
pip install -e .

# Run with verbose output
python scripts/train_model.py --verbose

# Check code style
flake8 scripts/
```

### Docker Development
```bash
# Build with custom tag
docker build -t titanic-train:dev .

# Run with volume mount for development
docker run -v $(pwd):/app titanic-train:dev

# Interactive container for debugging
docker run -it titanic-train:dev /bin/bash
```

### Kubernetes Development
```bash
# Delete existing job
kubectl delete job titanic-train-job

# Apply updated configuration
kubectl apply -f titanic-train-job.yaml

# Stream logs in real-time
kubectl logs -f job/titanic-train-job
```

## 📈 Expected Outputs

### Training Script Results
- **Model Accuracy**: ~80-85% on test set
- **Feature Importance Plot**: Visual ranking of predictive features
- **Saved Model**: `rf_model_titanic.joblib` file
- **Console Output**: Training metrics and statistics

### Key Features by Importance (typical)
1. **Fare** - Ticket price (proxy for socioeconomic status)
2. **Age** - Passenger age
3. **Pclass** - Passenger class (1st, 2nd, 3rd)
4. **Sex** - Gender (historically significant factor)

## 🔧 Troubleshooting

### Common Issues

**Import Errors**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

**File Path Issues**
```bash
# Run from correct directory
cd scripts
python train_model.py
```

**Docker Build Failures**
```bash
# Clean Docker cache
docker system prune
docker build --no-cache -t titanic-train .
```

**Kubernetes Job Stuck**
```bash
# Check pod status
kubectl get pods
kubectl describe pod <pod-name>
```

## 📚 Learning Objectives

This project teaches:
- **MLOps Pipeline**: End-to-end ML workflow automation
- **Containerization**: Docker for reproducible environments
- **Orchestration**: Kubernetes for scalable ML jobs
- **CI/CD**: Automated testing and deployment
- **Best Practices**: Data handling, model persistence, resource management

## 🎯 Next Steps

1. **Model Improvement**: Try different algorithms (XGBoost, Neural Networks)
2. **Feature Engineering**: Create new features from existing data
3. **Hyperparameter Tuning**: Optimize model parameters
4. **Model Monitoring**: Add performance tracking
5. **API Deployment**: Create REST API for predictions
6. **Model Registry**: Implement model versioning

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review error logs carefully
3. Ensure all prerequisites are met
4. Verify file paths and permissions
