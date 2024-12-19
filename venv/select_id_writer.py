from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
import sqlalchemy
from datetime import datetime

app = FastAPI()

DATABASE_URL = "mysql+aiomysql://root:Prasad@8@localhost/my_database"
database = Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

content_table = sqlalchemy.Table(
    "content_table",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True),
    sqlalchemy.Column("content", sqlalchemy.String(255), nullable=False),
    sqlalchemy.Column("writer_name", sqlalchemy.String(255), nullable=False),  
    sqlalchemy.Column("datetime", sqlalchemy.DateTime, nullable=False),
)

class ContentResponse(BaseModel):
    id: int
    content: str
    writer_name: str  
    datetime: datetime

@app.on_event("startup")
async def connect_to_db():
    """Ensure the database connection and table setup."""
    await database.connect()
    query = """
    CREATE TABLE IF NOT EXISTS content_table (
        id INT AUTO_INCREMENT PRIMARY KEY,
        content VARCHAR(255) NOT NULL,
        writer_name VARCHAR(255) NOT NULL,  
        datetime DATETIME NOT NULL
    );
    """
    try:
        await database.execute(query)
        print("Database connected and table ensured.")
    except Exception as e:
        print(f"Error during database startup: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed.")

@app.on_event("shutdown")
async def disconnect_from_db():
    """Close the database connection."""
    try:
        await database.disconnect()
        print("Database connection closed.")
    except Exception as e:
        print(f"Error during database shutdown: {e}")

@app.get("/content/{content_id}/", response_model=ContentResponse)
async def get_content_by_id(content_id: int):
    """
    Retrieve content by ID.
    """
    try:
        query = content_table.select().where(content_table.c.id == content_id)
        content = await database.fetch_one(query)

        if not content:
            raise HTTPException(status_code=404, detail="Content not found.")

        return ContentResponse(
            id=content["id"],
            content=content["content"],
            writer_name=content["writer_name"],
            datetime=content["datetime"],
        )
    except Exception as e:
        print(f"Error during fetching content by ID: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch content.")

@app.get("/content/author/{writer_name}/", response_model=list[ContentResponse])
async def get_content_by_writer(writer_name: str):
    """
    Retrieve content by writer_name.
    """
    try:
        query = content_table.select().where(content_table.c.writer_name == writer_name)
        contents = await database.fetch_all(query)

        if not contents:
            raise HTTPException(status_code=404, detail="No content found for this writer.")

        return [
            ContentResponse(
                id=content["id"],
                content=content["content"],
                writer_name=content["writer_name"],
                datetime=content["datetime"],
            )
            for content in contents
        ]
    except Exception as e:
        print(f"Error during fetching content by writer: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch content.")

@app.get("/content/", response_model=list[ContentResponse])
async def get_all_content():
    """
    Retrieve all content entries stored in the database.
    """
    try:
        query = content_table.select().order_by(content_table.c.datetime.desc())
        contents = await database.fetch_all(query)

        return [
            ContentResponse(
                id=content["id"],
                content=content["content"],
                writer_name=content["writer_name"], 
                datetime=content["datetime"],
            )
            for content in contents
        ]
    except Exception as e:
        print(f"Error during fetching all content: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch content.")
