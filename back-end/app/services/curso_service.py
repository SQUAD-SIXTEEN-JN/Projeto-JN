from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException

from app.models.models import Cursos, Progressos
from app.schemas.curso import CursoCreate, CursoUpdate


async def create_curso(db: Session, curso: CursoCreate) -> Cursos:
    """
    Cria um novo curso.
    """
    db_curso = Cursos(
        nome=curso.nome,
        descricao=curso.descricao
    )
    
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    
    return db_curso


async def get_curso(db: Session, curso_id: int, usuario_id: Optional[int] = None) -> Cursos:
    """
    Busca um curso pelo ID.
    Opcionalmente, pode receber o ID do usuário para buscar o progresso.
    """
    curso = db.query(Cursos).filter(Cursos.id == curso_id).first()
    
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    # Adiciona o progresso do usuário se o ID do usuário foi fornecido
    if usuario_id:
        progresso = db.query(Progressos).filter(
            Progressos.fk_curso == curso_id,
            Progressos.fk_usuario == usuario_id
        ).first()
        
        if progresso:
            curso.progresso = progresso.progresso
        else:
            curso.progresso = 0.0
    
    return curso


async def get_cursos(db: Session, skip: int = 0, limit: int = 100, usuario_id: Optional[int] = None) -> List[Cursos]:
    """
    Busca todos os cursos com paginação.
    Opcionalmente, pode receber o ID do usuário para buscar o progresso de cada curso.
    """
    cursos = db.query(Cursos).offset(skip).limit(limit).all()
    
    # Adiciona o progresso do usuário a cada curso se o ID do usuário foi fornecido
    if usuario_id:
        for curso in cursos:
            progresso = db.query(Progressos).filter(
                Progressos.fk_curso == curso.id,
                Progressos.fk_usuario == usuario_id
            ).first()
            
            if progresso:
                curso.progresso = progresso.progresso
            else:
                curso.progresso = 0.0
    
    return cursos


async def update_curso(db: Session, curso_id: int, curso_data: CursoUpdate) -> Cursos:
    """
    Atualiza um curso existente.
    """
    curso = await get_curso(db, curso_id)
    
    # Atualiza apenas os campos fornecidos
    update_data = curso_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(curso, key, value)
    
    db.commit()
    db.refresh(curso)
    
    return curso


async def delete_curso(db: Session, curso_id: int) -> Dict[str, bool]:
    """
    Remove um curso do banco de dados.
    """
    curso = await get_curso(db, curso_id)
    
    # Também remove todos os progressos associados a este curso
    db.query(Progressos).filter(Progressos.fk_curso == curso_id).delete()
    
    db.delete(curso)
    db.commit()
    
    return {"success": True}


async def search_cursos_by_name(db: Session, name: str, usuario_id: Optional[int] = None) -> List[Cursos]:
    """
    Busca cursos pelo nome.
    Opcionalmente, pode receber o ID do usuário para buscar o progresso de cada curso.
    """
    # Busca cursos com nome que contém a string fornecida
    cursos = db.query(Cursos).filter(
        or_(
            Cursos.nome.ilike(f"%{name}%"),
            Cursos.descricao.ilike(f"%{name}%")
        )
    ).all()
    
    # Adiciona o progresso do usuário a cada curso se o ID do usuário foi fornecido
    if usuario_id:
        for curso in cursos:
            progresso = db.query(Progressos).filter(
                Progressos.fk_curso == curso.id,
                Progressos.fk_usuario == usuario_id
            ).first()
            
            if progresso:
                curso.progresso = progresso.progresso
            else:
                curso.progresso = 0.0
    
    return cursos