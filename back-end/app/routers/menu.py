from fastapi import APIRouter, Depends, Query, Path
from typing import List
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.menu import MenuCreate, MenuResponse, MenuUpdate
from app.services.menu_service import (
    create_menu,
    get_menu,
    get_menus,
    update_menu,
    delete_menu,
    search_menus_by_name
)


router = APIRouter()

@router.post("/", response_model=MenuResponse, status_code=201)
async def create_menu_route(
    menu: MenuCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo menu.
    """
    return await create_menu(db=db, menu=menu)


@router.get("/{menu_id}", response_model=MenuResponse)
async def read_menu(
    menu_id: int = Path(..., title="ID do menu", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca um menu pelo ID.
    """
    return await get_menu(db=db, menu_id=menu_id)


@router.get("/", response_model=List[MenuResponse])
async def read_menus(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Busca todos os menus com paginação.
    """
    return await get_menus(db=db, skip=skip, limit=limit)


@router.patch("/{menu_id}", response_model=MenuResponse)
async def update_menu_route(
    menu_data: MenuUpdate,
    menu_id: int = Path(..., title="ID do menu", ge=1),
    db: Session = Depends(get_db)
):
    """
    Atualiza um menu existente.
    """
    return await update_menu(db=db, menu_id=menu_id, menu_data=menu_data)


@router.delete("/{menu_id}", response_model=dict)
async def delete_menu_route(
    menu_id: int = Path(..., title="ID do menu", ge=1),
    db: Session = Depends(get_db)
):
    """
    Remove um menu do banco de dados.
    """
    return await delete_menu(db=db, menu_id=menu_id)


@router.get("/search/", response_model=List[MenuResponse])
async def search_menus(
    name: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """
    Busca menus pelo nome.
    """
    return await search_menus_by_name(db=db, name=name)