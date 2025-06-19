# Start Minikube
minikube start

# Build Docker images
eval $(minikube docker-env)
docker build -t backend:latest ./backend
docker build -t frontend:latest ./frontend

# Apply Kubernetes manifests
kubectl apply -f deployment.yaml

# Verify services
kubectl get pods
kubectl get svc

# Access frontend UI
minikube service frontend-service --url