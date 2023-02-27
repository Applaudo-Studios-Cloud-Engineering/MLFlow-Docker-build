# pip install fastapi
# pip install uvicorn
# pip install "uvicorn[standard]" # for deploy
# uvicorn main:app --reload
# uvicorn main:app --host 0.0.0.0 --port 80 for deploy
from typing import List, Union
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
import array 
import requests
import os

class Columns(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: float
    Total_Income: float

class Item(BaseModel):
    columns: List[str] #Columns
    data: List[List[str]]

class ItemFormatted(BaseModel):
    columns: List[str] = []
    data: List[List[float]]

class RequestInvocationsFormatted(BaseModel):
    dataframe_split: ItemFormatted

class RequestInvocations(BaseModel):
    dataframe_split: Item

class Response(BaseModel):
    predictions: List[float]

class ResponseFormatted(BaseModel):
    predictions: List[str]

app = FastAPI()

@app.get("/my-first-api-0")
def hello0():
  return {"Hello world!"}


@app.get("/my-first-api-1")
def hello1(name = None):

    if name is None:
        text = 'Hello!'

    else:
        text = 'Hello ' + name + '!'

    return text


@app.get("/get-iris")
def get_iris():

    import pandas as pd
    url ='https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
    iris = pd.read_csv(url)

    return iris

@app.get("/plot-iris")
def plot_iris():

    import pandas as pd
    import matplotlib.pyplot as plt

    url ='https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv'
    iris = pd.read_csv(url)

    plt.scatter(iris['sepal_length'], iris['sepal_width'])
    plt.savefig('iris.png')
    file = open('iris.png', mode="rb")

    return StreamingResponse(file, media_type="image/png")

@app.post("/invocations")
def invocations(item1: RequestInvocations) -> ResponseFormatted:
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

    item2 = RequestInvocationsFormatted(dataframe_split=ItemFormatted(columns=item1.dataframe_split.columns,data=list))
    json = jsonable_encoder(item2)
    env = os.environ['MLFLOW_ENDPOINT']
    
    print(env)
    response = requests.post(env,json=json)

    responseJson= Response(predictions=response.json().get('predictions'))

    list = []
    for value in responseJson.predictions:
        list.append("N" if value == 0 else "Y")

    return ResponseFormatted(predictions=list)

# @app.post("/invocations2")
# def invocations(requestInvocationsFormatted: RequestInvocationsFormatted):
#     json = jsonable_encoder(requestInvocationsFormatted)
#     print(json)
#     response = requests.post("http://localhost:5000/invocations",json=json)
#     return response.json()