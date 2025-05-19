from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from typing import List, Optional, Dict
from fastapi import HTTPException, status

from app.models.models import Permissoes, Perfil, Menu
from app.schemas.permissoes import PermissoesCreate, PermissoesUpdate


async def create_permissao(db: Session, permissao: PermissoesCreate) -> Permissoes:
    """
    Cria uma nova permissão no banco de dados.
    Verifica se o perfil e o menu existem antes de criar a permissão.
    Verifica se já existe uma permissão com mesmo perfil e menu.
    """
    try:
        # Verifica se o perfil existe
        perfil = db.query(Perfil).filter(Perfil.id == permissao.fk_perfil).first()
        if not perfil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Perfil com ID {permissao.fk_perfil} não encontrado"
            )
        
        # Verifica se o menu existe
        menu = db.query(Menu).filter(Menu.id == permissao.fk_menu).first()
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu com ID {permissao.fk_menu} não encontrado"
            )
        
        # Verifica se já existe essa permissão
        existing_permissao = db.query(Permissoes).filter(
            Permissoes.fk_perfil == permissao.fk_perfil,
            Permissoes.fk_menu == permissao.fk_menu
        ).first()
        
        if existing_permissao:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Já existe uma permissão para o perfil {permissao.fk_perfil} e menu {permissao.fk_menu}"
            )
            
        # Cria a permissão
        db_permissao = Permissoes(
            fk_perfil=permissao.fk_perfil,
            fk_menu=permissao.fk_menu
        )
        db.add(db_permissao)
        db.commit()
        db.refresh(db_permissao)
        return db_permissao
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Erro de integridade. Verifique se o perfil e menu existem."
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar permissão: {str(e)}"
        )


async def get_permissao(db: Session, permissao_id: int) -> Optional[Permissoes]:
    """
    Busca uma permissão pelo ID.
    """
    permissao = db.query(Permissoes).filter(Permissoes.id == permissao_id).first()
    if permissao is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Permissão com ID {permissao_id} não encontrada"
        )
    return permissao


async def get_permissoes(db: Session, skip: int = 0, limit: int = 100) -> List[Permissoes]:
    """
    Busca todas as permissões com paginação.
    """
    return db.query(Permissoes).offset(skip).limit(limit).all()


async def update_permissao(db: Session, permissao_id: int, permissao_data: PermissoesUpdate) -> Permissoes:
    """
    Atualiza uma permissão existente.
    Verifica se o perfil e o menu existem antes de atualizar.
    """
    try:
        db_permissao = await get_permissao(db, permissao_id)
        update_data = permissao_data.dict(exclude_unset=True)
        
        # Se estiver atualizando o perfil, verifica se existe
        if "fk_perfil" in update_data:
            perfil = db.query(Perfil).filter(Perfil.id == update_data["fk_perfil"]).first()
            if not perfil:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Perfil com ID {update_data['fk_perfil']} não encontrado"
                )
        
        # Se estiver atualizando o menu, verifica se existe
        if "fk_menu" in update_data:
            menu = db.query(Menu).filter(Menu.id == update_data["fk_menu"]).first()
            if not menu:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Menu com ID {update_data['fk_menu']} não encontrado"
                )
        
        # Verifica se já existe essa combinação de perfil e menu
        if "fk_perfil" in update_data or "fk_menu" in update_data:
            perfil_id = update_data.get("fk_perfil", db_permissao.fk_perfil)
            menu_id = update_data.get("fk_menu", db_permissao.fk_menu)
            
            existing_permissao = db.query(Permissoes).filter(
                Permissoes.fk_perfil == perfil_id,
                Permissoes.fk_menu == menu_id,
                Permissoes.id != permissao_id
            ).first()
            
            if existing_permissao:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Já existe uma permissão para o perfil {perfil_id} e menu {menu_id}"
                )
        
        # Atualiza a permissão
        for key, value in update_data.items():
            setattr(db_permissao, key, value)
            
        db.commit()
        db.refresh(db_permissao)
        return db_permissao
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Erro de integridade. Verifique se o perfil e menu existem."
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar permissão: {str(e)}"
        )


async def delete_permissao(db: Session, permissao_id: int) -> dict:
    """
    Remove uma permissão do banco de dados.
    """
    try:
        db_permissao = await get_permissao(db, permissao_id)
        db.delete(db_permissao)
        db.commit()
        return {"message": f"Permissão com ID {permissao_id} removida com sucesso"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover permissão: {str(e)}"
        )


async def get_permissoes_by_perfil(db: Session, perfil_id: int) -> Dict:
    """
    Busca todas as permissões de um perfil específico,
    retornando o perfil e a lista de menus associados.
    """
    perfil = db.query(Perfil).filter(Perfil.id == perfil_id).first()
    if not perfil:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Perfil com ID {perfil_id} não encontrado"
        )
    
    permissoes = db.query(Permissoes).join(Menu).filter(
        Permissoes.fk_perfil == perfil_id
    ).all()
    
    menus = []
    for perm in permissoes:
        menu = db.query(Menu).filter(Menu.id == perm.fk_menu).first()
        if menu:
            menus.append({
                "id": menu.id,
                "nome": menu.nome,
                "descricao": menu.descricao,
                "rota": menu.rota,
                "permissao_id": perm.id
            })
    
    return {
        "perfil_id": perfil.id,
        "perfil_nome": perfil.nome,
        "menus": menus
    }


async def get_permissoes_by_menu(db: Session, menu_id: int) -> Dict:
    """
    Busca todas as permissões de um menu específico,
    retornando o menu e a lista de perfis associados.
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Menu com ID {menu_id} não encontrado"
        )
    
    permissoes = db.query(Permissoes).join(Perfil).filter(
        Permissoes.fk_menu == menu_id
    ).all()
    
    perfis = []
    for perm in permissoes:
        perfil = db.query(Perfil).filter(Perfil.id == perm.fk_perfil).first()
        if perfil:
            perfis.append({
                "id": perfil.id,
                "nome": perfil.nome,
                "descricao": perfil.descricao,
                "permissao_id": perm.id
            })
    
    return {
        "menu_id": menu.id,
        "menu_nome": menu.nome,
        "perfis": perfis
    }


async def delete_permissoes_by_perfil(db: Session, perfil_id: int) -> dict:
    """
    Remove todas as permissões de um perfil específico.
    """
    try:
        # Verifica se o perfil existe
        perfil = db.query(Perfil).filter(Perfil.id == perfil_id).first()
        if not perfil:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Perfil com ID {perfil_id} não encontrado"
            )
        
        # Remove todas as permissões do perfil
        deleted = db.query(Permissoes).filter(Permissoes.fk_perfil == perfil_id).delete()
        db.commit()
        
        return {"message": f"{deleted} permissões do perfil com ID {perfil_id} removidas com sucesso"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover permissões: {str(e)}"
        )


async def delete_permissoes_by_menu(db: Session, menu_id: int) -> dict:
    """
    Remove todas as permissões de um menu específico.
    """
    try:
        # Verifica se o menu existe
        menu = db.query(Menu).filter(Menu.id == menu_id).first()
        if not menu:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu com ID {menu_id} não encontrado"
            )
        
        # Remove todas as permissões do menu
        deleted = db.query(Permissoes).filter(Permissoes.fk_menu == menu_id).delete()
        db.commit()
        
        return {"message": f"{deleted} permissões do menu com ID {menu_id} removidas com sucesso"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover permissões: {str(e)}"
        )