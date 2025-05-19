from pydantic import BaseModel, Field, validator
from typing import Optional


class ProgressoBase(BaseModel):
    progresso: float = Field(..., ge=0, le=100, description="Porcentagem de progresso do curso (0-100)")
    fk_usuario: int = Field(..., ge=1, description="Matrícula do Usuário do usuário")
    fk_curso: int = Field(..., ge=1, description="ID do curso")


class ProgressoCreate(ProgressoBase):
    @validator('progresso')
    def validate_progress(cls, v):
        if v < 0 or v > 100:
            raise ValueError('O progresso deve estar entre 0 e 100')
        return v


class ProgressoUpdate(BaseModel):
    progresso: Optional[float] = Field(None, ge=0, le=100, description="Porcentagem de progresso do curso (0-100)")
    
    @validator('progresso')
    def validate_progress(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('O progresso deve estar entre 0 e 100')
        return v


class ProgressoResponse(ProgressoBase):
    id: int
    
    model_config = {
        "from_attributes": True
    }


class CursoSimpleInfo(BaseModel):
    id: int
    nome: str
    descricao: str
    
    model_config = {
        "from_attributes": True
    }


class ProgressoWithCursoResponse(BaseModel):
    id: int
    progresso: float = Field(..., ge=0, le=100, description="Porcentagem de progresso do curso (0-100)")
    fk_usuario: int
    curso: CursoSimpleInfo
    
    model_config = {
        "from_attributes": True
    }