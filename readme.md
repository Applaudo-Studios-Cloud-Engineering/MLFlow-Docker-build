# Build image

`docker build -t mleon96/mlflow:latest -t mleon96/mlflow:1.0.0 .`

`docker run --port External-port:Internal-port -itd image-name`

`docker run -p 5000:5000 -itd mleon96/mlflow:latest`

## Flow

This repo flow is made to first change te build_data.txt in the build and version if needed for the creation with the action of the DockerFile and it will generate said changes in the branch test with a pull request for the main branch that will have the build of the image when accepted the pull request

## MlFlow

Added functions of mlflow autolog that depending of the base library of machine learning needs to be checked if available

## FASTAPI 

Added functions to provide a REST API used for the communication between frontend and backend and a dataproccesing feature for easier use of the model deployed for the predictions
