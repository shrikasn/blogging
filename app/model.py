from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() # is a clase ,all models inherit from here 

class Blog(Base): # shows that Blog inherits from Base, 
    __tablename__ = 'blogs'#table name in the db
    
    # Define the columns in the table
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    content = Column(Text)
    writer_name = Column(String(255))

    def __repr__(self): # Define how the Blog  should be represented used for debugging 
        return f"<Blog(id={self.id}, title={self.title}, writer_name={self.writer_name})>"
