import os
from fastapi import Depends, FastAPI, HTTPException, status
from database import models, schemas
from authentication import authenticate_user, create_access_token, get_hashed_password
from sqlalchemy.orm import Session
from typing import Annotated
from authentication import get_current_active_user
from fastapi_sqlalchemy import DBSessionMiddleware, db

app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=os.getenv('DATABASE_URL'))

current_user_annotation = Annotated[schemas.User, Depends(get_current_active_user)]

@app.get("/")
async def root():
    return {"message": "hello"}

def is_unique(name: str, db: Session):
    existing_users_with_name = db.session.query(models.User).filter(models.User.name == name).all()
    if(existing_users_with_name):
        return False 
    return True 

@app.post("/create_user")
async def create_user(user: schemas.UserCreate):
    if not is_unique(user.name, db):
        raise HTTPException(status_code=422, detail="name must be unique")
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(name=user.name, hashed_password=hashed_password)
    db.session.add(db_user)
    db.session.commit()
    db.session.refresh(db_user)
    return db_user

@app.post("/create_opportunity")
async def create_opportunity(opportunity: schemas.OpportunityCreate, current_user: current_user_annotation):
    username = current_user.name 
    db_opportunity = models.Opportunity(url=opportunity.url,
                                        role_description=opportunity.role_description,
                                        user_name=username,
                                        notes=opportunity.notes,
                                        title=opportunity.title,
                                        date_applied=opportunity.date_applied,
                                        application_status=opportunity.application_status)
    db.session.add(db_opportunity)
    db.session.commit()
    db.session.refresh(db_opportunity)
    return db_opportunity

@app.get("/login")
async def login(name: str, password: str):
    user = authenticate_user(name,password,db.session)
    if(user):
        access_token = create_access_token({"sub": name})
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)

@app.get("/opportunities")
async def get_user_opportunities(current_user: current_user_annotation):
    opportunities = db.session.query(models.Opportunity).filter(models.Opportunity.user_name == current_user.name).all()
    return opportunities
