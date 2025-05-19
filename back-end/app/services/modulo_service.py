from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.models import Modulos, Cursos
from app.schemas.modulo import ModuloCreate, ModuloUpdate

async def get_modulos(db: Session, skip: int = 0, limit: int = 100) -> List[Modulos]:
    """Retorna todos os módulos com paginação"""
    return db.query(Modulos).offset(skip).limit(limit).all()

async def get_modulo(db: Session, modulo_id: int) -> Modulos:
    """Retorna um módulo pelo ID"""
    modulo = db.query(Modulos).filter(Modulos.id == modulo_id).first()
    if not modulo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Módulo com ID {modulo_id} não encontrado"
        )
    return modulo

async def create_modulo(db: Session, modulo: ModuloCreate) -> Modulos:
    """Cria um novo módulo"""
    # Verificar se o curso existe
    curso = db.query(Cursos).filter(Cursos.id == modulo.fk_curso).first()
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso com ID {modulo.fk_curso} não encontrado"
        )
    
    db_modulo = Modulos(
        nome=modulo.nome,
        ordem=modulo.ordem,
        descricao=modulo.descricao,
        fk_curso=modulo.fk_curso
    )
    db.add(db_modulo)
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

async def update_modulo(db: Session, modulo_id: int, modulo_data: ModuloUpdate) -> Modulos:
    """Atualiza um módulo existente"""
    db_modulo = await get_modulo(db, modulo_id)
    
    # Se houver atualização do curso, verificar se o novo curso existe
    if modulo_data.fk_curso is not None:
        curso = db.query(Cursos).filter(Cursos.id == modulo_data.fk_curso).first()
        if not curso:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Curso com ID {modulo_data.fk_curso} não encontrado"
            )
    
    update_data = modulo_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_modulo, key, value)
    
    db.commit()
    db.refresh(db_modulo)
    return db_modulo

async def delete_modulo(db: Session, modulo_id: int) -> Dict[str, bool]:
    """Exclui um módulo pelo ID"""
    db_modulo = await get_modulo(db, modulo_id)
    
    db.delete(db_modulo)
    db.commit()
    return {"success": True}

async def search_modulos_by_name(db: Session, name: str) -> List[Modulos]:
    """Pesquisa módulos pelo nome"""
    return db.query(Modulos).filter(Modulos.nome.ilike(f"%{name}%")).all()

async def get_modulos_by_curso(db: Session, curso_id: int, skip: int = 0, limit: int = 100) -> List[Modulos]:
    """Retorna todos os módulos de um curso específico"""
    # Verificar se o curso existe
    curso = db.query(Cursos).filter(Cursos.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso com ID {curso_id} não encontrado"
        )
    
    return db.query(Modulos)\
             .filter(Modulos.fk_curso == curso_id)\
             .order_by(Modulos.ordem)\
             .offset(skip)\
             .limit(limit)\
             .all()