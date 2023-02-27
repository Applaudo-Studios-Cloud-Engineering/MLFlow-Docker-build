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

RUN apt-get update 
RUN apt-get install -y git

# Copy over artifact and code
# COPY ./docker_resources/run.sh /opt/fastapi/scripts/
COPY ./run.sh /opt/fastapi/scripts/

# COPY model_format.py /opt/fastapi/utils/
# COPY ./docker_resources/temp_artifacts/* ${ARTIFACT_STORE}/
COPY ./main.py ${ARTIFACT_STORE}/

RUN chmod +x /opt/fastapi/scripts/run.sh 

ENTRYPOINT ["/usr/bin/env"]
CMD ["bash", "/opt/fastapi/scripts/run.sh"]