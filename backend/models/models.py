from pydantic import BaseModel

class create_user(BaseModel):
    email:str
    password:str
    
class UserLogin(BaseModel):
    email: str
    password: str    
    
class userModel(BaseModel):
    id:int  
    email:str
    password:str  
        
class Config:
    orm_mode=True