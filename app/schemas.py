from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from pydantic.types import conint
from typing import Annotated
from pydantic import ConfigDict

class Post(BaseModel):
    title: str
    data: str
         #server: str
    published:bool = True
    model_config = ConfigDict(from_attributes=True)
    
class createPost(Post):
    pass

class update(Post):
    pass

class UserOut(BaseModel): # our response model for the user
    id: int
    email: EmailStr
    created_at: datetime
    phone_number: str
    

class UserPost(BaseModel): # our response model for the user
    #id: int
    email: EmailStr
    #created_at: datetime
   
   
class PostOut(Post):
    Post: Post
    votes: int
    class Config:
        orm_mode = True


class Response(Post):
    id: int
    title: str
    data: str
         #server: str
    published:bool
    created_at: datetime
    owner_id: int
    owner: UserPost
   # votes: int
    
    model_config = ConfigDict(from_attributes=True)
    #class Config:
     #    orm_mode = True

class Out(BaseModel):
    PostMethod: Response
    votes: int
    model_config = ConfigDict(from_attributes=True)
    
    #class Config:
    #    orm_mode = True
        
class userCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: str
    
 
    
    class Config:
        orm_mode = True #to convert the sqlalchemy model to a pydantic model
        
class Userlogin(BaseModel):
    email: EmailStr
    password: str
    
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[int] = None
    
    
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)] #to return either 0 or 1
    
    