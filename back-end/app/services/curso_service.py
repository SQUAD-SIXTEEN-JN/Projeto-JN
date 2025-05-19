from typing import List, Optional, Dict
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.models import Cursos
from app.schemas.curso import CursoCreate, CursoUpdate

async def get_cursos(db: Session, skip: int = 0, limit: int = 100) -> List[Cursos]:
    """Retorna todos os cursos com paginação"""
    return db.query(Cursos).offset(skip).limit(limit).all()

async def get_curso(db: Session, curso_id: int) -> Cursos:
    """Retorna um curso pelo ID"""
    curso = db.query(Cursos).filter(Cursos.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Curso com ID {curso_id} não encontrado"
        )
    return curso

async def create_curso(db: Session, curso: CursoCreate) -> Cursos:
    """Cria um novo curso"""
    db_curso = Cursos(nome=curso.nome, descricao=curso.descricao)
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

async def update_curso(db: Session, curso_id: int, curso_data: CursoUpdate) -> Cursos:
    """Atualiza um curso existente"""
    db_curso = await get_curso(db, curso_id)
    
    update_data = curso_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_curso, key, value)
    
    db.commit()
    db.refresh(db_curso)
    return db_curso

async def delete_curso(db: Session, curso_id: int) -> Dict[str, bool]:
    """Exclui um curso pelo ID"""
    db_curso = await get_curso(db, curso_id)
    
    db.delete(db_curso)
    db.commit()
    return {"success": True}

async def search_cursos_by_name(db: Session, name: str) -> List[Cursos]:
    """Pesquisa cursos pelo nome"""
    return db.query(Cursos).filter(Cursos.nome.ilike(f"%{name}%")).all()