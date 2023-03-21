#!/bin/sh
# run.sh
# mlflow models serve -m $ARTIFACT_STORE -h $SERVER_HOST -p $SERVER_PORT --no-conda
uvicorn main:app --host $SERVER_HOST --port $SERVER_PORT --app-dir $ARTIFACT_STORE