from typing import Optional
from pydantic import BaseModel, Field

class CursoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do curso")
    descricao: Optional[str] = Field(None, description="Descrição detalhada do curso")

class CursoCreate(CursoBase):
    pass

class CursoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100, description="Nome do curso")
    descricao: Optional[str] = Field(None, description="Descrição detalhada do curso")

class CursoResponse(CursoBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }