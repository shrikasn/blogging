# app/main.py

from fastapi import FastAPI
from users.views import router as user_router
from app.views import router as blog_router

app = FastAPI()

# Include the user-related routes
app.include_router(user_router, prefix="/users", tags=["users"])

# Include the blog-related routes
app.include_router(blog_router, prefix="/blogs", tags=["blogs"])
