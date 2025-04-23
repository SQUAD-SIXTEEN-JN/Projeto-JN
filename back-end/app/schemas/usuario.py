from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    matricula: int
    senha: str
    fk_perfil: int
