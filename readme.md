# Build image

`docker build -t mleon96/mlflow:latest -t mleon96/mlflow:1.0.0 .`

`docker run --port External-port:Internal-port -itd image-name`

`docker run -p 5000:5000 -itd mleon96/mlflow:latest`

## Flow

This repo flow is made to first change te build_data.txt in the build and version if needed for the creation with the action of the DockerFile and it will generate said changes in the branch test with a pull request for the main branch that will have the build of the image when accepted the pull request

## DEPLOY HELM

`gcloud container clusters get-credentials cluster-1 --zone us-central1-c --project mlops-kubeflow-tests`

`kubectl create secret docker-registry gcr-json-key  --docker-server=us.gcr.io  --docker-username=_json_key  --docker-password="$(cat ~/mlops-kubeflow-tests-38867ad95dd0.json)"  --docker-email=253107550346-compute@developer.gserviceaccount.com -n mlflow`

`helm install mlflow-helm-chart mlflow-helm-chart -n mlflow`