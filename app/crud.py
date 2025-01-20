#performs CRUD operations 
#1xx: Information , 2xx: Successful, 3xx: Redirection, 4xx:ckient error,5xx: Server Error
from sqlalchemy.ext.asyncio import AsyncSession #(module in SQLAlchemy that provides tools to work with asynchronous databases)
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from app.model import Blog
from app.schemas import BlogCreate, Blog as BlogSchema

# Async func to retrieve a blog by id from db
async def get_blog(db: AsyncSession, blog_id: int):
    result = await db.execute(select(Blog).filter(Blog.id == blog_id))#selects the given id and filters from db
    blog = result.scalar_one_or_none()#extracts one result of none if nothing found
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found") #Raise HTTP 404 error if not found
    return blog # Return the blog if found

#async func to create a new blog
async def create_blog(db: AsyncSession, blog: BlogCreate): #gets info from schema
    new_blog = Blog(title=blog.title, content=blog.content, writer_name=blog.writer_name)
    db.add(new_blog) #add blog to db
    await db.commit() #commit session to add blog in db
    return new_blog # returns the blog

#async func to uldate a new blog
async def update_blog(db: AsyncSession, blog_id: int, blog: BlogCreate):
    existing_blog = await get_blog(db, blog_id)
    existing_blog.title = blog.title
    existing_blog.content = blog.content
    existing_blog.writer_name = blog.writer_name
    await db.commit()
    return existing_blog

#async func to delete a new blog
async def delete_blog(db: AsyncSession, blog_id: int):
    existing_blog = await get_blog(db, blog_id)
    await db.delete(existing_blog)
    await db.commit()
    return existing_blog

#async funs to read all blogs
async def get_blogs(db: AsyncSession):
    result = await db.execute(select(Blog)) 
    return result.scalars().all()
