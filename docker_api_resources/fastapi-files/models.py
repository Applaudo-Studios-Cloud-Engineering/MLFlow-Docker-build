from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base
# from .database import Base


class Model(Base):
    __tablename__ = "models"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(String, unique=True, index=True)
    model_version = Column(String)
    is_active = Column(Boolean, default=True)

    opinions = relationship("Opinion", back_populates="owner")


class Opinion(Base):
    __tablename__ = "opinions"

    id = Column(Integer, primary_key=True, index=True)
    is_good = Column(Boolean, default=True)
    # request_id = Column(Integer, ForeignKey("requests.id"))
    owner_id = Column(Integer, ForeignKey("models.id"))

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