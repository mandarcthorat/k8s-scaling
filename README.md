# Install Minikube
choco install minikube  

# Start Minikube
minikube start --driver=docker

# Set Docker environment
eval $(minikube docker-env)

# Build backend from backend directory
docker build -t frontend:latest frontend/

# Build frontend from frontend directory
docker build -t backend:latest backend/

# Deployment
kubectl apply -f deployment.yaml

# Remove old deployment
kubectl delete -f deployment.yaml

# Monitoring
kubectl get pods -o wide

kubectl get events --sort-by=.metadata.creationTimestamp

kubectl get endpoints frontend-service backend-service

minikube dashboard

# Load Testing from host
## Setup port forwarding for frontend and backend in different terminal windows
kubectl port-forward service/frontend-service 8080:80

kubectl port-forward service/backend-service 5000:5000

## Launch load testing script
python tests/load_testing.py
