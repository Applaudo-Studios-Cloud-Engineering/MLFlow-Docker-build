from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float,BIGINT, TEXT ,BOOLEAN
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
    # request_id = Column(Integer, ForeignKey("requests.id"))
    owner_id = Column(BIGINT, ForeignKey("models.id"))

    owner = relationship("Model", back_populates="opinions")
    # request = relationship("Request", back_populates="opinion")

# class Request(Base):
#     __tablename__ = "requests"

#     id = Column(Integer, primary_key=True, index=True)
#     Gender = Column(String)
#     Married = Column(String)
#     Dependents = Column(String)
#     Education = Column(String)
#     Self_Employed = Column(String)
#     ApplicantIncome = Column(Float)
#     CoapplicantIncome = Column(Float)
#     LoanAmount = Column(Float)
#     Loan_Amount_Term = Column(Float)
#     Credit_History = Column(Float)
#     Property_Area = Column(Float)
#     Total_Income = Column(Float)

#     opinion = relationship("Opinion", back_populates="request")