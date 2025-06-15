from typing import Optional
from pydantic import BaseModel, Field


class UsuarioCreate(BaseModel):
    nome: str
    matricula: int
    senha: str
    perfil: str


class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do usuário")
    matricula: int = Field(..., description="Matrícula do usuário")
    fk_perfil: int = Field(..., description="ID do perfil do usuário")


class UsuarioUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=None, max_length=100, description="Nome do usuário")
    perfil: Optional[str] = Field(None, min_length=None, description="Nome do perfil do usuário")


# Classe para evitar referência circular
class PerfilSimple(BaseModel):
    id: int
    nome: str
    
    model_config = {
        "from_attributes": True
    }


class UsuarioResponse(BaseModel):
    matricula: int
    nome: str
    primeiro_acesso: bool
    fk_perfil: int
    perfil: Optional[PerfilSimple] = None
    
    model_config = {
        "from_attributes": True
    }