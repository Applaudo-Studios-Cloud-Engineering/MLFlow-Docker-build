from typing import Union

from pydantic import BaseModel
from typing import List


class RequestBase(BaseModel):
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

class Request(RequestBase):
    id: int

    class Config:
        orm_mode = True

class OpinionBase(BaseModel):
    is_good: bool
    request_id: int
    # description: Union[str, None] = None


class OpinionCreate(OpinionBase):
    pass


class Opinion(OpinionBase):
    id: int
    owner_id: int
    request_id: int
    request: Request

    class Config:
        orm_mode = True


class ModelBase(BaseModel):
    model_id: str
    model_version: str


class ModelCreate(ModelBase):
    is_active: bool


class Model(ModelBase):
    id: int
    is_active: bool
    opinions: list[Opinion] = []

    class Config:
        orm_mode = True

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

class ResponseJson(BaseModel):
    response: str
    id: int
