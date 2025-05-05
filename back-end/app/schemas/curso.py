from pydantic import BaseModel

class Curso(BaseModel):
    id: int
    nome: str
    descricao: str

    class Config:
        orm_mode = True