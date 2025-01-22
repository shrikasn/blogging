# app/users/schema.py
from pydantic import BaseModel


class UserCreate(BaseModel): #provides data validation 
    username: str
    password: str

class UserLogin(BaseModel): #handling login data
    username: str
    password: str


#Enables Pydantic to map data from ORM objects
    class Config:
        from_attributes = True  
