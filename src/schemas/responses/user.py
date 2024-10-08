from typing import Union
from datetime import datetime
from pydantic import EmailStr
from src.schemas.responses.base import BaseResponse


class UserResponse(BaseResponse):
    id: int
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    created_at: Union[str, None, datetime] = None

class LoginResponse(BaseResponse):
    access_token: str
    token_type: str = "Bearer"
    refresh_token: str
    expires_in: int