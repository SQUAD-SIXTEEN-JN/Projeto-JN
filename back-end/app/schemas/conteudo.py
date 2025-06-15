from pydantic import BaseModel

class ConteudoBase(BaseModel):
    nome: str
    url: str
    fk_modulo: int
    ordem: int
    tipo: str

class ConteudoCreate(ConteudoBase):
    pass

class ConteudoUpdate(ConteudoBase):
    pass

class ConteudoResponse(ConteudoBase):
    id: int

    model_config = {
        "from_attributes": True
    }
