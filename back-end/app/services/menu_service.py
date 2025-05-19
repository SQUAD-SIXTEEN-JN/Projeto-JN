from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.models import Menu
from app.schemas.menu import MenuCreate, MenuUpdate


async def create_menu(db: Session, menu: MenuCreate) -> Menu:
    """
    Cria um novo menu no banco de dados.
    """
    try:
        db_menu = Menu(
            nome=menu.nome,
            descricao=menu.descricao,
            rota=menu.rota
        )
        db.add(db_menu)
        db.commit()
        db.refresh(db_menu)
        return db_menu
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar menu: {str(e)}"
        )


async def get_menu(db: Session, menu_id: int) -> Optional[Menu]:
    """
    Busca um menu pelo ID.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if menu is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu com ID {menu_id} não encontrado"
        )
    return menu


async def get_menus(db: Session, skip: int = 0, limit: int = 100) -> List[Menu]:
    """
    Busca todos os menus com paginação.
    """
    return db.query(Menu).offset(skip).limit(limit).all()


async def update_menu(db: Session, menu_id: int, menu_data: MenuUpdate) -> Menu:
    """
    Atualiza um menu existente.
    """
    try:
        db_menu = await get_menu(db, menu_id)
        
        # Atualiza apenas os campos fornecidos
        update_data = menu_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_menu, key, value)
            
        db.commit()
        db.refresh(db_menu)
        return db_menu
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar menu: {str(e)}"
        )


async def delete_menu(db: Session, menu_id: int) -> dict:
    """
    Remove um menu do banco de dados.
    """
    try:
        db_menu = await get_menu(db, menu_id)
        db.delete(db_menu)
        db.commit()
        return {"message": f"Menu com ID {menu_id} removido com sucesso"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover menu: {str(e)}"
        )


async def search_menus_by_name(db: Session, name: str) -> List[Menu]:
    """
    Busca menus pelo nome (busca parcial).
    """
    return db.query(Menu).filter(Menu.nome.ilike(f"%{name}%")).all()