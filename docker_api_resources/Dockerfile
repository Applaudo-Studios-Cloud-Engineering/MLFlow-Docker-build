FROM python:3.9.13

ENV SERVER_PORT 8000
ENV SERVER_HOST 0.0.0.0
ENV FILE_STORE /opt/fastapi/fileStore
ENV ARTIFACT_STORE /opt/fastapi/artifactStore
ENV PYTHONPATH /opt/fastapi/utils
ENV MLFLOW_ENDPOINT http://localhost:5000/invocations

RUN mkdir -p /opt/fastapi/scripts \
&& mkdir -p ${FILE_STORE} \
&& mkdir -p ${ARTIFACT_STORE}
RUN pip install fastapi
RUN pip install "uvicorn[standard]"
RUN pip install requests
# RUN pip install psycopg2-binary 
# RUN pip install configparser
# RUN pip install MySQL-python
RUN pip install mysqlclient
RUN pip install sqlalchemy

RUN apt-get update 
RUN apt-get install -y git

# Copy over artifact and code
# COPY ./docker_api_resources/run.sh /opt/fastapi/scripts/
COPY ./run.sh /opt/fastapi/scripts/

# COPY model_format.py /opt/fastapi/utils/
# COPY ./docker_api_resources/temp_artifacts/* ${ARTIFACT_STORE}/
COPY ./fastapi-files/* ${ARTIFACT_STORE}/

RUN chmod +x /opt/fastapi/scripts/run.sh 

ENTRYPOINT ["/usr/bin/env"]
CMD ["bash", "/opt/fastapi/scripts/run.sh"]

# docker build -t mleon96/mlflow-mnist-fastapi:latest -t mleon96/mlflow-mnist-fastapi:1.1.3 .\docker_api_resources
# docker run -d -p 8000:8000 -e MLFLOW_ENDPOINT='http://172.17.0.2:5000' -e PGHOST='host.docker.internal' -e PGPORT='5432' -e PGDATABASE='mlflow' -e PGUSER='postgres' -e PGPASSWORD='admin'  mleon96/mlflow-mnist-fastapi:latest