from pydantic import BaseModel

class BlogBase(BaseModel): #creating Base schema for the blog
    #defining fields
    title: str
    content: str
    writer_name: str

class BlogCreate(BlogBase): # for creating a new blog
    pass #inherits fields from BlogBase

class Blog(BlogBase): #Schema for the blog which is  returned to the user
    id: int #additional firld

#Enables Pydantic to map data from ORM objects
    class Config:
        from_attributes = True  