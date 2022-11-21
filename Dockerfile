FROM python:3.7.15
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

RUN pip install pandas \
&& pip install scikit-learn==1.0.2 \
&& pip install cloudpickle==2.2.0 \
&& pip install mlflow \
&& apt-get update \
&& apt-get install -y git

# Copy over artifact and code
COPY ./run.sh /opt/mlflow/scripts/

# COPY model_format.py /opt/mlflow/utils/
COPY ./temp_artifacts/* ${ARTIFACT_STORE}/

RUN chmod +x /opt/mlflow/scripts/run.sh 

ENTRYPOINT ["/usr/bin/env"]
CMD ["bash", "/opt/mlflow/scripts/run.sh"]