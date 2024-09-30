
from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    phone: str
    address: str



class VerifyUserRequest(BaseModel):
    token: str
    email: EmailStr
    
    
