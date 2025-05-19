from typing import Optional
from pydantic import BaseModel, Field

class ModuloBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=40, description="Nome do módulo")
    ordem: int = Field(..., ge=0, description="Ordem de apresentação do módulo")
    descricao: Optional[str] = Field(None, description="Descrição detalhada do módulo")
    fk_curso: int = Field(..., ge=1, description="ID do curso ao qual o módulo pertence")

class ModuloCreate(ModuloBase):
    pass

class ModuloUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=40, description="Nome do módulo")
    ordem: Optional[int] = Field(None, ge=0, description="Ordem de apresentação do módulo")
    descricao: Optional[str] = Field(None, description="Descrição detalhada do módulo")
    fk_curso: Optional[int] = Field(None, ge=1, description="ID do curso ao qual o módulo pertence")

class ModuloResponse(ModuloBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }

class ModuloWithCursoResponse(ModuloResponse):
    curso: Optional["CursoSimpleResponse"] = None
    
    model_config = {
        "from_attributes": True
    }

class CursoSimpleResponse(BaseModel):
    id: int
    nome: str
    
    model_config = {
        "from_attributes": True
    }

# Resolvendo a referência circular
ModuloWithCursoResponse.update_forward_refs()