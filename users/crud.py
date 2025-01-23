from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from users.model import User
from users.schema import UserCreate
import re


async def register_user(db: AsyncSession, user: UserCreate):
    # Check if username already exists
    existing_user = await db.execute(select(User).filter(User.username == user.username))
    if existing_user.scalars().first():
        raise HTTPException(status_code=400, detail="Username already exists")

    # Password validation 
    password_pattern = r'^[A-Za-z0-9_\-+!@#$%^&*(),.":{}|<>]{1,10}$'
    if not re.match(password_pattern, user.password):
        raise HTTPException(status_code=400, detail="Password must contain at least one special character, one number, one alphabet, and not exceed 10 characters")

    # Store the password directly (no hashing)
    new_user = User(username=user.username, password=user.password)
    
    db.add(new_user)
    await db.commit()  # Save user to DB
    return new_user


# Login user: Check username and password 
async def login_user(db: AsyncSession, user: UserCreate):
    # Retrieve user from DB
    db_user = await db.execute(select(User).filter(User.username == user.username))
    db_user = db_user.scalars().first()

    if db_user and db_user.password == user.password:  # will compare from the db
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")
