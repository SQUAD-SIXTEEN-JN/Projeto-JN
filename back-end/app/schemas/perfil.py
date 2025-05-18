from pydantic import BaseModel, Field
from typing import Optional


class PerfilBase(BaseModel):
    nome: str = Field(..., max_length=50, description="Nome do perfil")
    descricao: Optional[str] = Field(None, description="Descrição do perfil")


class PerfilCreate(PerfilBase):
    pass


class PerfilUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=50, description="Nome do perfil")
    descricao: Optional[str] = Field(None, description="Descrição do perfil")


class PerfilResponse(PerfilBase):
    id: int

    model_config = {
        "from_attributes": True
    }