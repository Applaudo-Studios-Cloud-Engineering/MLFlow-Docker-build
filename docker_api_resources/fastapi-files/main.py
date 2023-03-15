# uvicorn sql_app.main:app --reload
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

import requests
import os

import crud, models, schemas
from database import SessionLocal, engine

# docker inspect distracted_johnson | grep IPAddress
# If running uvicorn sql_app.main:app --reload change crud models
# from . import crud, models, schemas
# from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/models/", response_model=schemas.Model)
def create_model(model: schemas.ModelCreate, db: Session = Depends(get_db)):
    db_model = crud.get_model_by_model_id(db, model_id=model.model_id)
    if db_model:
        raise HTTPException(status_code=400, detail="Model already registered")
    return crud.create_model(db=db, model=model)


@app.get("/models/", response_model=list[schemas.Model])
def read_models(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    models = crud.get_models(db, skip=skip, limit=limit)
    return models


@app.get("/models/{model_id}", response_model=schemas.Model)
def read_model(model_id: int, db: Session = Depends(get_db)):
    db_model = crud.get_model(db, model_id=model_id)
    if db_model is None:
        raise HTTPException(status_code=404, detail="Model not found")
    return db_model

# {'title': 'item1', 'description': 'description1', 'owner_id': 4} example
@app.post("/models/{model_id}/opinions/", response_model=schemas.Opinion)
def create_opinion_for_model(
    model_id: int, opinion: schemas.OpinionCreate, db: Session = Depends(get_db)
):
    return crud.create_model_opinion(db=db, opinion=opinion, model_id=model_id)


@app.get("/opinions/", response_model=list[schemas.Opinion])
def read_opinions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    opinions = crud.get_opinions(db, skip=skip, limit=limit)
    return opinions

@app.post("/invocations", response_model=schemas.ResponseFormatted)
def invocations(item1: schemas.RequestInvocations):
    list = []
    for value  in item1.dataframe_split.data:
        aux = []
        for count2, dataValue in enumerate(value):
            if item1.dataframe_split.columns[count2] == "Gender":
                aux.append(float(0) if dataValue == 'Male' else float(1))
            elif item1.dataframe_split.columns[count2] == "Married":
                aux.append(float(0) if dataValue == 'No' else float(1))
            elif item1.dataframe_split.columns[count2] == "Dependents":
                dataValue.replace("3+", "3")
                aux.append(float(dataValue))
            elif item1.dataframe_split.columns[count2] == "Education":
                aux.append(float(0) if dataValue == 'Not Graduate' else float(1))
            elif item1.dataframe_split.columns[count2] == "Self_Employed":
                aux.append(float(0) if dataValue == 'No' else float(1))
            elif item1.dataframe_split.columns[count2] == "ApplicantIncome":
                aux.append(float(dataValue))
            elif item1.dataframe_split.columns[count2] == "CoapplicantIncome":
                aux.append(float(dataValue))
            elif item1.dataframe_split.columns[count2] == "LoanAmount":
                aux.append(float(dataValue))
            elif item1.dataframe_split.columns[count2] == "Loan_Amount_Term":
                aux.append(float(dataValue))
            elif item1.dataframe_split.columns[count2] == "Credit_History":
                aux.append(float(dataValue))
            elif item1.dataframe_split.columns[count2] == "Property_Area":
                aux.append(float(0) if dataValue == 'Urban' else float(1) if dataValue == 'Semiurban' else float(2))
            elif item1.dataframe_split.columns[count2] == "Total_Income":
                aux.append(float(dataValue))
            else:
                aux.append(float(dataValue))
        list.append(aux)

    item2 = schemas.RequestInvocationsFormatted(dataframe_split=schemas.ItemFormatted(columns=item1.dataframe_split.columns,data=list))
    json = jsonable_encoder(item2)
    env = os.environ['MLFLOW_ENDPOINT']
    
    print(env)
    response = requests.post((env + '/invocations'), json=json)

    responseJson= schemas.Response(predictions=response.json().get('predictions'))

    list = []
    for value in responseJson.predictions:
        list.append("N" if value == 0 else "Y")

    return schemas.ResponseFormatted(predictions=list)

# @app.post("/invocations2")
# def invocations(requestInvocationsFormatted: RequestInvocationsFormatted):
#     json = jsonable_encoder(requestInvocationsFormatted)
#     print(json)
#     response = requests.post("http://localhost:5000/invocations",json=json)
#     return response.json()

@app.post("/invocations2", response_model=schemas.ResponseJson)
def invocations2(item1: schemas.Columns):
    list = []
    aux = []
    columns = []

    columns.append('Gender')
    aux.append(float(0) if item1.Gender == 'Male' else float(1))
        
    columns.append('Married')
    aux.append(float(0) if item1.Married == 'No' else float(1))
    
    columns.append('Dependents')
    item1.Dependents.replace("3+", "3")
    aux.append(float(item1.Dependents))

    columns.append('Education')
    aux.append(float(0) if item1.Education == 'Not Graduate' else float(1))

    columns.append('Self_Employed')
    aux.append(float(0) if item1.Self_Employed == 'No' else float(1))

    columns.append('ApplicantIncome')
    aux.append(float(item1.ApplicantIncome))
    
    columns.append('CoapplicantIncome')
    aux.append(float(item1.CoapplicantIncome))

    columns.append('LoanAmount')
    aux.append(float(item1.LoanAmount))

    columns.append('Loan_Amount_Term')
    aux.append(float(item1.Loan_Amount_Term))

    columns.append('Credit_History')
    aux.append(float(item1.Credit_History))
    
    columns.append('Property_Area')
    aux.append(float(0) if item1.Property_Area == 'Urban' else float(1) if item1.Property_Area == 'Semiurban' else float(2))

    columns.append('Total_Income')
    aux.append(float(item1.Total_Income))
    
    list.append(aux)

    item2 = schemas.RequestInvocationsFormatted(dataframe_split=schemas.ItemFormatted(columns=columns,data=list))
    json = jsonable_encoder(item2)
    env = os.environ['MLFLOW_ENDPOINT']
    
    print(env)
    response = requests.post((env + '/invocations'), json=json)

    responseJson= schemas.Response(predictions=response.json().get('predictions'))

    response=''
    for value in responseJson.predictions:
        response = "No" if value == 0 else "Yes"

    return schemas.ResponseJson(response=response)