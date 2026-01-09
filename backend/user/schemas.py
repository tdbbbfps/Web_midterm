from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    username : str = Field(..., description="The username of the user.")
    
class UserCreate(UserBase):
    email : EmailStr = Field(..., description="The email of the user.")
    password : str = Field(..., description="The password of the user.")
    
class UserRead(BaseModel):
    id : int = Field(..., description="The id of the user.")

class UserUpdate(BaseModel):
    email : Optional[EmailStr] = None
    username : Optional[str] = None
    password : Optional[str] = None
    
class UserDelete(BaseModel):
    id : int

class User(UserBase):
    id : int
    
    model_config = ConfigDict(from_attributes=True)
    
class UserLogin(UserBase):
    password : str = Field(..., description="The password of the user.")