# main.py
from fastapi import FastAPI
from app.views import router as blog_router  # Importing the router from views.py

app = FastAPI()

# Include the blog routes in the FastAPI application
app.include_router(blog_router)
