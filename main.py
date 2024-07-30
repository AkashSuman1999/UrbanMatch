from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
import models, schemas
import re

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: dict, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.id == user_id).first()
    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    update_data = user.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_user, key, value)
    db.commit()
    db.refresh(existing_user)
    return existing_user

@app.delete("users/{user_id}", response_model = dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "inactive"
    db.commit()
    return {"status_code": 200, "message": f"User of id : {user_id} has been deleted."}

@app.get("/get_potential_matches/{user_id}", response_model = list[schemas.User])
def get_potential_matches(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.interests:
        raise HTTPException(status_code=400, detail="User has no interests specified")
    interest_placeholders = ', '.join([f"'{interest}'" for interest in user.interests])
    match_query = f"""select * from users where gender != {user.gender} and age > {user.age} - 5 and age < {user.age} + 5 
    and city = {user.city} and ARRAY(SELECT UNNEST(interests) INTERSECT SELECT UNNEST(ARRAY[{interest_placeholders}])) > 1"""
    potential_matches = db.query(models.User).from_statement(text(match_query)).all()
    return potential_matches

