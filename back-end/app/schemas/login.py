from pydantic import BaseModel

class Login(BaseModel):
    matricula: int
    senha: str
