from sqlalchemy.orm import Session

import models, schemas
# from . import models, schemas

def get_model(db: Session, model_id: int):
    return db.query(models.Model).filter(models.Model.id == model_id).first()


def get_model_by_model_id(db: Session, model_id: str):
    return db.query(models.Model).filter(models.Model.model_id == model_id).first()


def get_models(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Model).offset(skip).limit(limit).all()


def create_model(db: Session, model: schemas.ModelCreate):
    # fake_hashed_password = user.password + "notreallyhashed"
    db_model = models.Model(model_id=model.model_id, model_version=model.model_version, is_active=model.is_active)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model


def get_opinions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Opinion).offset(skip).limit(limit).all()


def create_model_opinion(db: Session, opinion: schemas.OpinionCreate, model_id: int):
    db_item = models.Opinion(**opinion.dict(), owner_id=model_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_request(db: Session, request: schemas.RequestBase):
    db_request = models.Request(**request.dict())
    db.add(db_request)
    db.commit()
    db.refresh(db_request)
    return db_request