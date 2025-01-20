# views.py
from fastapi import APIRouter, Depends
from fastapi import FastAPI, Depends, HTTPException #used to raise HTTP exceptions 
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession #SQLAlchemy, a python Object-Relational Mapping library to perform async db operations
from sqlalchemy.orm import sessionmaker # creates Sessions
from sqlalchemy.ext.declarative import declarative_base#it keeps track of all the models and tables
from app.model import Blog # inports the class blof from app.model
from app.schemas import BlogCreate, Blog # inports these from app.schemas
from app.crud import create_blog, update_blog, delete_blog, get_blog , get_blogs # imports these from app.views
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

# Create a new blog post
@router.post("/blogs/", response_model=Blog)
async def create_new_blog(blog: BlogCreate, db: AsyncSession = Depends(get_db)): 
    return await create_blog(db, blog)

# Get a single blog post by ID
@router.get("/blogs/{blog_id}", response_model=Blog)
async def read_blog(blog_id: int, db: AsyncSession = Depends(get_db)): 
    return await get_blog(db, blog_id)

# Update an existing blog post
@router.put("/blogs/{blog_id}", response_model=Blog)
async def update_existing_blog(blog_id: int, blog: BlogCreate, db: AsyncSession = Depends(get_db)):
    return await update_blog(db, blog_id, blog)

# Delete a blog post
@router.delete("/blogs/{blog_id}", response_model=Blog)
async def delete_existing_blog(blog_id: int, db: AsyncSession = Depends(get_db)): 
    return await delete_blog(db, blog_id)

# Get all blogs
@router.get("/blogs/", response_model=list[Blog])
async def read_blogs(db: AsyncSession = Depends(get_db)):
    return await get_blog(db)
