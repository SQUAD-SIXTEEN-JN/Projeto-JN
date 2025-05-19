from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.perfil import PerfilCreate, PerfilResponse, PerfilUpdate
from app.services.perfil_service import (
    create_perfil,
    get_perfil,
    get_perfis,
    update_perfil,
    delete_perfil,
    search_perfis_by_name
)

router = APIRouter()


@router.post("/", response_model=PerfilResponse, status_code=201)
async def create_perfil_route(
    perfil: PerfilCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo perfil.
    """
    return await create_perfil(db=db, perfil=perfil)


@router.get("/{perfil_id}", response_model=PerfilResponse)
async def read_perfil(
    perfil_id: int = Path(..., title="ID do perfil", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca um perfil pelo ID.
    """
    return await get_perfil(db=db, perfil_id=perfil_id)


@router.get("/", response_model=List[PerfilResponse])
async def read_perfis(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Busca todos os perfis com paginação.
    """
    return await get_perfis(db=db, skip=skip, limit=limit)


@router.patch("/{perfil_id}", response_model=PerfilResponse)
async def update_perfil_route(
    perfil_data: PerfilUpdate,
    perfil_id: int = Path(..., title="ID do perfil", ge=1),
    db: Session = Depends(get_db)
):
    """
    Atualiza um perfil existente.
    """
    return await update_perfil(db=db, perfil_id=perfil_id, perfil_data=perfil_data)


@router.delete("/{perfil_id}", response_model=dict)
async def delete_perfil_route(
    perfil_id: int = Path(..., title="ID do perfil", ge=1),
    db: Session = Depends(get_db)
):
    """
    Remove um perfil do banco de dados.
    """
    return await delete_perfil(db=db, perfil_id=perfil_id)


@router.get("/search/", response_model=List[PerfilResponse])
async def search_perfis(
    name: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """
    Busca perfis pelo nome.
    """
    return await search_perfis_by_name(db=db, name=name)