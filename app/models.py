from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class PostMethod(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    data = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    #votes = relationship("Votes")
    
    
class User(Base): 
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))
    phone_number= Column(String, nullable=False)
    
    
class Votes(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    
    

    
    
class Another(Base):
    __tablename__ = "another"
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)   
    data = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)    
    created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('NOW()'))