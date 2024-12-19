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

class ContentRequest(BaseModel):
    content: str
    writer_name: str  

class ContentUpdateRequest(BaseModel):
    content: str
    writer_name: str  

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
        writer_name VARCHAR(255) NOT NULL,  -- Ensure writer_name column exists
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

@app.post("/content/", response_model=ContentResponse)
async def add_content(content_request: ContentRequest):
    """
    Add a new content entry to the database.
    Users can submit their content directly.
    """
    try:
        if not content_request.content:
            raise HTTPException(status_code=400, detail="Content cannot be empty.")
        if not content_request.writer_name:
            raise HTTPException(status_code=400, detail="Writer name cannot be empty.")

        current_time = datetime.now()

        print(f"Inserting content: {content_request.content} by {content_request.writer_name}")

        query = content_table.insert().values(
            content=content_request.content,
            writer_name=content_request.writer_name,  
            datetime=current_time,
        )
        content_id = await database.execute(query)

        print(f"Content inserted with ID: {content_id}")

        return ContentResponse(
            id=content_id,
            content=content_request.content,
            writer_name=content_request.writer_name,  
            datetime=current_time,
        )
    except Exception as e:
        print(f"Error during content addition: {e}")
        raise HTTPException(status_code=500, detail="Failed to add content.")

@app.put("/content/{content_id}/", response_model=ContentResponse)
async def update_content(content_id: int, content_request: ContentUpdateRequest):
    """
    Update an existing content entry in the database.
    """
    try:
        if not content_request.content:
            raise HTTPException(status_code=400, detail="Content cannot be empty.")
        if not content_request.writer_name:
            raise HTTPException(status_code=400, detail="Writer name cannot be empty.")

        
        query = content_table.select().where(content_table.c.id == content_id)
        existing_content = await database.fetch_one(query)

        if not existing_content:
            raise HTTPException(status_code=404, detail="Content not found.")

        
        current_time = datetime.now()
        update_query = content_table.update().where(content_table.c.id == content_id).values(
            content=content_request.content,
            writer_name=content_request.writer_name,
            datetime=current_time,
        )

        await database.execute(update_query)

        return ContentResponse(
            id=content_id,
            content=content_request.content,
            writer_name=content_request.writer_name,
            datetime=current_time,
        )
    except Exception as e:
        print(f"Error during content update: {e}")
        raise HTTPException(status_code=500, detail="Failed to update content.")

@app.delete("/content/{content_id}/")
async def delete_content(content_id: int):
    """
    Delete an existing content entry from the database.
    """
    try:
        query = content_table.select().where(content_table.c.id == content_id)
        existing_content = await database.fetch_one(query)

        if not existing_content:
            raise HTTPException(status_code=404, detail="Content not found.")

        
        delete_query = content_table.delete().where(content_table.c.id == content_id)
        await database.execute(delete_query)

        return {"message": f"Content with ID {content_id} has been deleted."}
    except Exception as e:
        print(f"Error during content deletion: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete content.")

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
