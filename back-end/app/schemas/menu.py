from pydantic import BaseModel, Field
from typing import Optional


class MenuBase(BaseModel):
    nome: str = Field(..., max_length=30, description="Nome do menu")
    descricao: str = Field(..., description="Descrição do menu")
    rota: str = Field(..., description="Rota do menu")


class MenuCreate(MenuBase):
    pass


class MenuUpdate(BaseModel):
    nome: Optional[str] = Field(None, max_length=30, description="Nome do menu")
    descricao: Optional[str] = Field(None, description="Descrição do menu")
    rota: Optional[str] = Field(None, description="Rota do menu")


class MenuResponse(MenuBase):
    id: int

    model_config = {
        "from_attributes": True
    }