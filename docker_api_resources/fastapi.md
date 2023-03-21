FastAPI Application Documentation
=================================

Introduction
------------

This application is a FastAPI based REST API that provides functionality for registering and querying machine learning models and their opinions. In addition, the application also provides an endpoint to invoke a deployed model for a given input dataframe.

This code consumes a given endpoint and a given database url for a better handling of the data used for the prediction and an easier representation of the called needed at the moment of integrating said solution.

The directory structure is the following

```
│   Dockerfile
│   fastapi.md
│   run.sh
│
└───fastapi-files
        crud.py
        database.py
        main.py
        models.py
        schemas.py
        __init__.py
```

The first files are the ones used for the correct build of the images and the ones in the subdirectory fastapi-files are the ones containing the code used for the fastapi deployment and the orm solution that in this case is sqlalchemy with the logic of the endpoints contained in the main.py file and the schemas.py file the other files are responsible of the orm database connection and handling of the requests needed for the creation of the resources used in the database. And this image receives at the moment of running ENV variables for the setup of the endpoints needed in this case one for the consuming of the model serving server and the other ones for the database connection URL.

The file used for the Docker image contains the instructions needed for the installation of the required libraries and the versions used for a stable deployment and the copy of the needed files with emphasis in the run.sh that is the file handling the startup of the application server used.

Installation
------------

The following instructions are for setting up the application on a local machine.

### Requirements

* Python 3.7 or higher

### Steps

1. Clone the repository:

    shellCopy code

    `$ git clone https://github.com/Applaudo-Studios-Cloud-Engineering/MLFlow-Docker-build`
    `$ cd .\docker_api_resources\fastapi-files\`

2. Install the requirements:

    `$ pip install -r requirements.txt`

3. Start the server:

    `$ uvicorn sql_app.main:app --reload`

    The above command will start the server at `http://localhost:8000`.

API Documentation
-----------------

The following section describes the API endpoints available in this application.

### Get all Models

Endpoint to retrieve all registered models.

**HTTP Request Method**: GET

**URL**: `/models/`

**Request Parameters**:

* `skip` (optional): The number of models to skip. Default is 0.
* `limit` (optional): The maximum number of models to retrieve. Default is 100.

**Response**: Returns a list of `Model` objects.

### Get a Model

Endpoint to retrieve a registered model by ID.

**HTTP Request Method**: GET

**URL**: `/models/{model_id}`

**Request Parameters**:

* `model_id`: The ID of the model to retrieve.

**Response**: Returns a `Model` object.

### Create a Model

Endpoint to register a new model.

**HTTP Request Method**: POST

**URL**: `/models/`

**Request Body**: A `ModelCreate` object.

**Response**: Returns the newly created `Model` object.

### Create an Opinion

Endpoint to add an opinion to a model.

**HTTP Request Method**: POST

**URL**: `/models/{model_id}/opinions/`

**Request Body**: An `OpinionCreate` object.

**Request Parameters**:

* `model_id`: The ID of the model to add the opinion to.

**Response**: Returns the newly created `Opinion` object.

### Get all Opinions

Endpoint to retrieve all opinions.

**HTTP Request Method**: GET

**URL**: `/opinions/`

**Request Parameters**:

* `skip` (optional): The number of opinions to skip. Default is 0.
* `limit` (optional): The maximum number of opinions to retrieve. Default is 100.

**Response**: Returns a list of `Opinion` objects.

### Invoke a Model

Endpoint to invoke a deployed model for a given input dataframe.

**HTTP Request Method**: POST

**URL**: `/invocations/`

**Request Body**: A `RequestInvocations` object.

**Response**: Returns a `ResponseFormatted` object.

Dependencies
------------

The application uses the following dependencies:

* `FastAPI` for building the REST API.
* `SQLAlchemy` for database operations.
* `Pydantic` for data validation.
* `requests` for making HTTP requests.
* `uvicorn` for running the application server.
