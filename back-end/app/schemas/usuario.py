from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str
    matricula: int
    senha: str  # Recebe a senha em texto plano
    fk_perfil: int
