from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float,BIGINT, TEXT ,BOOLEAN, FLOAT
from sqlalchemy.orm import relationship

from database import Base
# from .database import Base


class Model(Base):
    __tablename__ = "models"

    id = Column(BIGINT, primary_key=True, index=True)
    model_id = Column(TEXT, unique=True, index=True)
    model_version = Column(TEXT)
    is_active = Column(BOOLEAN, default=True)

    opinions = relationship("Opinion", back_populates="owner")


class Opinion(Base):
    __tablename__ = "opinions"

    id = Column(BIGINT, primary_key=True, index=True)
    is_good = Column(BOOLEAN, default=True)
    request_id = Column(BIGINT, ForeignKey("requests.id"))
    owner_id = Column(BIGINT, ForeignKey("models.id"))

    owner = relationship("Model", back_populates="opinions")
    request = relationship("Request", back_populates="opinion")

class Request(Base):
    __tablename__ = "requests"

    id = Column(BIGINT, primary_key=True, index=True)
    Gender = Column(TEXT)
    Married = Column(TEXT)
    Dependents = Column(TEXT)
    Education = Column(TEXT)
    Self_Employed = Column(TEXT)
    ApplicantIncome = Column(FLOAT)
    CoapplicantIncome = Column(FLOAT)
    LoanAmount = Column(FLOAT)
    Loan_Amount_Term = Column(FLOAT)
    Credit_History = Column(FLOAT)
    Property_Area = Column(FLOAT)
    Total_Income = Column(FLOAT)

    opinion = relationship("Opinion", back_populates="request")