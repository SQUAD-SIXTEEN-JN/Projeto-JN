from typing import Optional, List
from pydantic import BaseModel, Field

class CursoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do curso")
    descricao: Optional[str] = Field(None, description="Descrição detalhada do curso")

class CursoCreate(CursoBase):
    pass

class CursoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100, description="Nome do curso")
    descricao: Optional[str] = Field(None, description="Descrição detalhada do curso")

# Classe para evitar referência circular
class ModuloSimple(BaseModel):
    id: int
    nome: str
    ordem: int
    
    model_config = {
        "from_attributes": True
    }

class CursoResponse(CursoBase):
    id: int
    modulos: List[ModuloSimple] = []
    
    model_config = {
        "from_attributes": True
    }