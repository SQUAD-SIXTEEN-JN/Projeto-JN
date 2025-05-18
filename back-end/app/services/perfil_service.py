from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.models import Perfil
from app.schemas.perfil import PerfilCreate, PerfilUpdate


async def create_perfil(db: Session, perfil: PerfilCreate) -> Perfil:
    """
    Cria um novo perfil no banco de dados.
    """
    try:
        # Verifica se já existe um perfil com o mesmo nome
        existing_perfil = db.query(Perfil).filter(Perfil.nome == perfil.nome).first()
        if existing_perfil:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Já existe um perfil com o nome '{perfil.nome}'"
            )
            
        # Cria o novo perfil se não existir duplicata
        db_perfil = Perfil(
            nome=perfil.nome,
            descricao=perfil.descricao
        )
        db.add(db_perfil)
        db.commit()
        db.refresh(db_perfil)
        return db_perfil
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar perfil: {str(e)}"
        )


async def get_perfil(db: Session, perfil_id: int) -> Optional[Perfil]:
    """
    Busca um perfil pelo ID.
    """
    perfil = db.query(Perfil).filter(Perfil.id == perfil_id).first()
    if perfil is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Perfil com ID {perfil_id} não encontrado"
        )
    return perfil


async def get_perfis(db: Session, skip: int = 0, limit: int = 100) -> List[Perfil]:
    """
    Busca todos os perfis com paginação.
    """
    return db.query(Perfil).offset(skip).limit(limit).all()


async def update_perfil(db: Session, perfil_id: int, perfil_data: PerfilUpdate) -> Perfil:
    """
    Atualiza um perfil existente.
    """
    try:
        db_perfil = await get_perfil(db, perfil_id)
        
        # Atualiza apenas os campos fornecidos
        update_data = perfil_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_perfil, key, value)
            
        db.commit()
        db.refresh(db_perfil)
        return db_perfil
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar perfil: {str(e)}"
        )


async def delete_perfil(db: Session, perfil_id: int) -> dict:
    """
    Remove um perfil do banco de dados.
    """
    try:
        db_perfil = await get_perfil(db, perfil_id)
        db.delete(db_perfil)
        db.commit()
        return {"message": f"Perfil com ID {perfil_id} removido com sucesso"}
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao remover perfil: {str(e)}"
        )


async def search_perfis_by_name(db: Session, name: str) -> List[Perfil]:
    """
    Busca perfis pelo nome (busca parcial).
    """
    return db.query(Perfil).filter(Perfil.nome.ilike(f"%{name}%")).all()