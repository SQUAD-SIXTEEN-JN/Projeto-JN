from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas.permissoes import (
    PermissoesCreate, 
    PermissoesResponse, 
    PermissoesUpdate,
    PermissoesByPerfilResponse,
    PermissoesByMenuResponse
)
from app.services.permissoes_service import (
    create_permissao,
    get_permissao,
    get_permissoes,
    update_permissao,
    delete_permissao,
    get_permissoes_by_perfil,
    get_permissoes_by_menu,
    delete_permissoes_by_perfil,
    delete_permissoes_by_menu
)

router = APIRouter()


@router.post("/", response_model=PermissoesResponse, status_code=201)
async def create_permissao_route(
    permissao: PermissoesCreate,
    db: Session = Depends(get_db)
):
    """
    Cria uma nova permissão associando um perfil a um menu.
    """
    return await create_permissao(db=db, permissao=permissao)


@router.get("/{permissao_id}", response_model=PermissoesResponse)
async def read_permissao(
    permissao_id: int = Path(..., title="ID da permissão", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca uma permissão pelo ID.
    """
    return await get_permissao(db=db, permissao_id=permissao_id)


@router.get("/", response_model=List[PermissoesResponse])
async def read_permissoes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Busca todas as permissões com paginação.
    """
    return await get_permissoes(db=db, skip=skip, limit=limit)


@router.patch("/{permissao_id}", response_model=PermissoesResponse)
async def update_permissao_route(
    permissao_data: PermissoesUpdate,
    permissao_id: int = Path(..., title="ID da permissão", ge=1),
    db: Session = Depends(get_db)
):
    """
    Atualiza uma permissão existente.
    """
    return await update_permissao(db=db, permissao_id=permissao_id, permissao_data=permissao_data)


@router.delete("/{permissao_id}", response_model=dict)
async def delete_permissao_route(
    permissao_id: int = Path(..., title="ID da permissão", ge=1),
    db: Session = Depends(get_db)
):
    """
    Remove uma permissão do banco de dados.
    """
    return await delete_permissao(db=db, permissao_id=permissao_id)


@router.get("/perfil/{perfil_id}", response_model=PermissoesByPerfilResponse)
async def read_permissoes_by_perfil(
    perfil_id: int = Path(..., title="ID do perfil", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca todas as permissões de um perfil específico,
    retornando o perfil e a lista de menus associados.
    """
    return await get_permissoes_by_perfil(db=db, perfil_id=perfil_id)


@router.get("/menu/{menu_id}", response_model=PermissoesByMenuResponse)
async def read_permissoes_by_menu(
    menu_id: int = Path(..., title="ID do menu", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca todas as permissões de um menu específico,
    retornando o menu e a lista de perfis associados.
    """
    return await get_permissoes_by_menu(db=db, menu_id=menu_id)


@router.delete("/perfil/{perfil_id}", response_model=dict)
async def delete_permissoes_by_perfil_route(
    perfil_id: int = Path(..., title="ID do perfil", ge=1),
    db: Session = Depends(get_db)
):
    """
    Remove todas as permissões de um perfil específico.
    """
    return await delete_permissoes_by_perfil(db=db, perfil_id=perfil_id)


@router.delete("/menu/{menu_id}", response_model=dict)
async def delete_permissoes_by_menu_route(
    menu_id: int = Path(..., title="ID do menu", ge=1),
    db: Session = Depends(get_db)
):
    """
    Remove todas as permissões de um menu específico.
    """
    return await delete_permissoes_by_menu(db=db, menu_id=menu_id)