from typing import Optional
from pydantic import EmailStr, BaseModel

class User(BaseModel):
    username:str
    password:str
    email:EmailStr
    # active_session:Optional[bool] = False
    
class updateUser(BaseModel):
    username:Optional[str]
    password:Optional[str]
    email:Optional[EmailStr]
    active_session:Optional[bool] = False

class LoginReq(BaseModel):
    username:str
    password:str