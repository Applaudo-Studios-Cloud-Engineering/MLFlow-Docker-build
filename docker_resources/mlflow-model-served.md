# Resources needed for building and running model serving image

This code consumes experiment created files saved in a s3 bucket for the creation of a model serving image using mlflow.

The directory structure is the following

```
│   DockerFile
│   fastapi.md
│   regex.bash
│   run.sh
│
├───templates
│       DockerTemplate1
│       DockerTemplate2
│
└───temp_artifacts
        conda.yaml
        input_example.json
        MLmodel
        model.pkl
        python_env.yaml
        requirements.txt
```

The build of the image consists of creating the needed docker file in accordance of the requirements given by the file requirements.txt and MLmodel that contains the needed libraries and the python version to use. This is acomplished by the regex.bash file that when run it creates a new DockerFile with the templates and files needed in the correct format for the build following that the DockerFile can be run for the build of the said image that now will use the needed versions of the libraries and python and the run.sh file needed to start the mlflow server.