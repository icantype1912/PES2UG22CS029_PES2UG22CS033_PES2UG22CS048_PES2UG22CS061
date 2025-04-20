
echo "Stopping deployment"
kubectl delete -f /home/adi/dev/CloudComputing/URL_Shortener/project/k8s

echo "Stopping minikube"
minikube stop

echo "cluster deleted"