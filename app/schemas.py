
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

from app.models import User


# Paydantic class for user creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str


# Pydantic class for User response , specialy for not showing or get back our password
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


# Payload for User Authentication 
class UserLogin(BaseModel):
    email: EmailStr
    password: str



# the Base Pydantic model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


# pydantic model For Post Creation 
class PostCreate(PostBase):
    pass


# pydantic model for Post Responses 
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse

    """ for using response_model=schemas.PostResponse on the decorator
        because the paydantic dont now how to work with orm query 
        she now just here Dict, class config is important for that."""

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


# Payload for responsonse of token
class Token(BaseModel):
    access_token: str
    token_type: str 


# Payload for returning after the verification and decode of JWT
class TokenData(BaseModel):
    id: Optional[str] = None
    email: Optional[EmailStr] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # default = 1