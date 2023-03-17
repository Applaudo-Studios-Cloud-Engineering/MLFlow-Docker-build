# Resources needed for building and running fastapi image

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
