FROM python:3.10.10

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
RUN pip install mlflow==2.1.1
RUN pip install cloudpickle==2.2.1
RUN pip install scikit-learn==1.2.1
RUN pip install pathlib==1.0.1
RUN pip install typing-extensions==4.5.0
# mlflow<3,>=2.1
# cloudpickle==2.2.1
# pathlib==1.0.1
# scikit-learn==1.2.1
# typing-extensions==4.5.0

RUN apt-get update 
RUN apt-get install -y git

# Copy over artifact and code
# COPY ./docker_resources/run.sh /opt/mlflow/scripts/
COPY ./run.sh /opt/mlflow/scripts/

# COPY model_format.py /opt/mlflow/utils/
# COPY ./docker_resources/temp_artifacts/* ${ARTIFACT_STORE}/
COPY ./temp_artifacts/* ${ARTIFACT_STORE}/

RUN chmod +x /opt/mlflow/scripts/run.sh 

ENTRYPOINT ["/usr/bin/env"]
CMD ["bash", "/opt/mlflow/scripts/run.sh"]