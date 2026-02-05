# MLOps Fundamentals - Titanic Survival Prediction

A comprehensive machine learning project demonstrating MLOps practices using the Titanic dataset. This project covers the complete ML pipeline from data preprocessing to model deployment using modern DevOps tools.

## Educational Video Course MLOps Fundamentals 

This course is part of MLOps Specialization and it's available by the next link https://nubes.academy/mlops-fundamentals-mlops-specialization/ 

## 📁 Project Structure

```
mlops-fundamentals/
├── data/                           # Dataset files
│   ├── train.csv                   # Training data with survival labels
│   └── test.csv                    # Test data for predictions
├── scripts/                        # Python scripts
│   ├── train_model.py             # Main ML training pipeline
│   ├── app.py                     # Flask API for model serving
│   └── predict_random.sh          # API testing script
├── .github/workflows/             # GitHub Actions CI/CD
│   └── ci.yml                     # Automated testing and training
├── Dockerfile                     # Container for training
├── Dockerfile.api                 # Container for API serving
├── titanic-train-job.yaml        # Kubernetes Job definition
├── model-deployment.yaml          # Kubernetes Deployment for API
├── model-service.yaml             # Kubernetes Services for API/metrics
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

### Build Training Container
```bash
# Build the training container
docker build -t titanic-train .
```

### Run Training in Container
```bash
# Execute training pipeline in Docker
docker run titanic-train
```

### Build API Container
```bash
# Build the API serving container
docker build -t rf-titanic-observable:latest -f Dockerfile.api .
```

### Docker Architecture
- **Training Image**: `python:3.10-slim` - Runs `train_model.py`
- **API Image**: `python:3.10-slim` - Runs Flask API with monitoring
- **Working Directory**: `/app/scripts`
- **Dependencies**: Installed from `requirements.txt`

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

### Deploy API Service
```bash
# Deploy the ML model API
kubectl apply -f model-deployment.yaml
kubectl apply -f model-service.yaml

# Check deployment status
kubectl get deployments
kubectl get services
kubectl get pods
```

### Configuration Features
- **Training Job**: 1GB RAM, 1 CPU core maximum, auto-cleanup after 1 hour
- **API Deployment**: Scalable service with health monitoring
- **Services**: Separate endpoints for API (8000) and metrics (8001)

## 🔄 CI/CD Pipeline

GitHub Actions automatically:
- Triggers on push/PR to main branch
- Sets up Python 3.13.5 environment
- Installs project dependencies
- Executes training pipeline
- Reports success/failure status

### Workflow File: `.github/workflows/ci.yml`

## 🧪 API Testing

### Test API with Random Data
```bash
# Make the script executable
chmod +x scripts/predict_random.sh

# Send single prediction request
./scripts/predict_random.sh

# Send multiple requests for load testing
./scripts/predict_random.sh 10
```

### Manual API Testing
```bash
# Test prediction endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '[{"Pclass": 3, "Sex_male": 1, "Age": 22, "SibSp": 1, "Parch": 0, "Fare": 7.25, "Embarked_Q": 0, "Embarked_S": 1}]'

# Check metrics
curl http://localhost:8001/metrics
```

## 📊 Monitoring Setup

### Install Prometheus
```bash
# Add Prometheus Helm repository
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

# Install Prometheus
helm install prometheus prometheus-community/prometheus
```

### Install Grafana
```bash
# Add Grafana Helm repository
helm repo add grafana https://grafana.github.io/helm-charts

# Install Grafana
helm install grafana grafana/grafana
```

### Access Monitoring Tools
```bash
# Port-forward services to local machine
kubectl port-forward svc/grafana 3000:80
kubectl port-forward svc/prometheus-server 9090:80
kubectl port-forward svc/rf-model-api 8000:8000
```

### Grafana Login
- **Username**: `admin`
- **Password**: Get with command below
```bash
kubectl get secret --namespace default grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

### Configure Prometheus for ML Model
```bash
# Edit Prometheus configuration
kubectl edit configmap prometheus-server -n default

# Add this job configuration to scrape_configs section:
  - job_name: 'rf_model'
    static_configs:
      - targets: ['rf-metrics.default.svc.cluster.local:8001']
```

## 📋 Dependencies

| Package | Purpose |
|---------|----------|
| pandas | Data manipulation and analysis |
| numpy | Numerical operations |
| scikit-learn | Machine learning algorithms |
| seaborn | Statistical data visualization |
| matplotlib | Plotting and charts |
| joblib | Model serialization |
| flask | Web framework for API |
| prometheus_client | Metrics collection |

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

## 📁 File Descriptions

### New Files Added
- **`app.py`**: Flask API server with Prometheus monitoring for real-time predictions
- **`predict_random.sh`**: Bash script for automated API testing with random passenger data
- **`Dockerfile.api`**: Container configuration for API serving with monitoring
- **`model-deployment.yaml`**: Kubernetes Deployment for scalable API service
- **`model-service.yaml`**: Kubernetes Services for API and metrics endpoints

## 🎯 Next Steps

1. **Model Improvement**: Try different algorithms (XGBoost, Neural Networks)
2. **Feature Engineering**: Create new features from existing data
3. **Hyperparameter Tuning**: Optimize model parameters
4. **Advanced Monitoring**: Set up alerts and dashboards in Grafana
5. **Load Balancing**: Scale API deployment for high availability
6. **Model Registry**: Implement model versioning and A/B testing

## 🔧 Troubleshooting

### API Issues
```bash
# Check API pod logs
kubectl logs deployment/rf-model

# Test API connectivity
kubectl port-forward svc/rf-model-api 8000:8000
curl http://localhost:8000/predict
```

### Monitoring Issues
```bash
# Check Prometheus targets
kubectl port-forward svc/prometheus-server 9090:80
# Visit http://localhost:9090/targets

# Restart Prometheus after config changes
kubectl rollout restart deployment prometheus-server
```

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review error logs carefully
3. Ensure all prerequisites are met
4. Verify file paths and permissions
5. Test API endpoints with provided scripts

Prepared by [Oleksiy Pototskyy](https://pototskyy.net/)
