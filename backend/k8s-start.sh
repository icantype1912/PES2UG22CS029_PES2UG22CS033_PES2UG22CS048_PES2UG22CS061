echo "Starting minikube"
minikube start

echo "Starting deployment"
kubectl apply -f /home/adi/dev/CloudComputing/URL_Shortener/project/k8s

echo "cluster started"