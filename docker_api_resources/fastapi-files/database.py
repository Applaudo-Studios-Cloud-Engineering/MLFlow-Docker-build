from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://mlflow:password@mlflow-mysql.cduy8wtiztlt.us-east-1.rds.amazonaws.com:3306/mlflow"
# export MLFLOW_ENDPOINT "http://localhost:5000"
env_host = os.environ['PGHOST'] # PGHOST PGPORT PGDATABASE PGUSER PGPASSWORD
env_port = os.environ['PGPORT']
env_database = os.environ['PGDATABASE']
env_user = os.environ['PGUSER']
env_pass = os.environ['PGPASSWORD']
env_database_type = os.environ['DATABASETYPE']
SQLALCHEMY_DATABASE_URL = env_database_type + '://' + env_user + ':' + env_pass + '@' + env_host + ':' + env_port + '/' + env_database #"postgresql://postgres:admin@localhost:5432/mlflow"
# SQLALCHEMY_DATABASE_URL = "mysql://root:admin@localhost:3306/mlflow"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    # connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()