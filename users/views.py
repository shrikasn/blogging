# app/views.py

from fastapi import APIRouter, Depends
from users import logs, schema
from fastapi import FastAPI, Depends, HTTPException #used to raise HTTP exceptions 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession #SQLAlchemy, a python Object-Relational Mapping library to perform async db operations
from sqlalchemy.orm import sessionmaker # creates Sessions
from sqlalchemy.ext.declarative import declarative_base#it keeps track of all the models and tables
import os # used to connect the os
from dotenv import load_dotenv #simplifies the management of sensitive configuration details

load_dotenv() 
  

DATABASE_URL = os.getenv("DATABASE_URL") #configure the database connection.
#creates an async db , connects to the specific db url 
engine = create_async_engine(DATABASE_URL, echo=True) 

router = APIRouter()

SessionLocal = sessionmaker(
    #binds the engine, creates an async session, makes sure it does not expire
    bind=engine , class_=AsyncSession, expire_on_commit=False
)

def get_db():
    db = SessionLocal() #creates the local session
    try:
        yield db #gives the db session to the user
    finally:
        db.close() #makes sure the session is closed after use.


# Register user endpoint
@router.post("/register")
async def register(user: schema.UserCreate, db: AsyncSession = Depends(get_db)):
    return await logs.register_user(db=db, user=user) #will store the user

# Login user endpoint
@router.post("/login")
async def login(user: schema.UserCreate, db: AsyncSession = Depends(get_db)):
    return await logs.login_user(db=db, user=user) #will check the credentials
