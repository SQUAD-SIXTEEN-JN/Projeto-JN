from pydantic import BaseModel, Field
from typing import Optional, List


class PermissoesBase(BaseModel):
    fk_perfil: int = Field(..., description="ID do perfil")
    fk_menu: int = Field(..., description="ID do menu")


class PermissoesCreate(PermissoesBase):
    pass


class PermissoesUpdate(BaseModel):
    fk_perfil: Optional[int] = Field(None, description="ID do perfil")
    fk_menu: Optional[int] = Field(None, description="ID do menu")


class PermissoesResponse(PermissoesBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class PermissoesByPerfilResponse(BaseModel):
    perfil_id: int
    perfil_nome: str
    menus: List[dict]

    model_config = {
        "from_attributes": True
    }


class PermissoesByMenuResponse(BaseModel):
    menu_id: int
    menu_nome: str
    perfis: List[dict]

    model_config = {
        "from_attributes": True
    }