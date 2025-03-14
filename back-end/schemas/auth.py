from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    name: Optional[str] = None
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: str
    refresh_token: str