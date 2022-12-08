FROM python:3.9.15

ARG RUN_ID
ARG MODEL_NAME

ENV SERVER_PORT 5000
ENV SERVER_HOST 0.0.0.0
ENV FILE_STORE /opt/mlflow/fileStore
ENV ARTIFACT_STORE /opt/mlflow/artifactStore
ENV PYTHONPATH /opt/mlflow/utils

RUN mkdir -p /opt/mlflow/scripts \
&& mkdir -p ${FILE_STORE} \
&& mkdir -p ${ARTIFACT_STORE}
RUN pip install mlflow
RUN pip install fsspec==2022.11.0
RUN pip install google-api-python-client==1.12.11
RUN pip install google-cloud-storage==1.44.0
RUN pip install pandas==1.5.2
RUN pip install pillow==9.3.0
RUN pip install scipy==1.9.3
RUN pip install tensorflow==2.11.0

RUN apt-get update 
RUN apt-get install -y git

# Copy over artifact and code
COPY ./docker_resources/run.sh /opt/mlflow/scripts/

# COPY model_format.py /opt/mlflow/utils/
COPY ./docker_resources/temp_artifacts/* ${ARTIFACT_STORE}/

RUN chmod +x /opt/mlflow/scripts/run.sh 

ENTRYPOINT ["/usr/bin/env"]
CMD ["bash", "/opt/mlflow/scripts/run.sh"]