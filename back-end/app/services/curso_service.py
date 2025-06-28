import base64

from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, UploadFile

from app.models.models import Cursos, Progressos
from app.schemas.curso import CursoCreate, CursoUpdate


async def create_curso(db: Session, curso: CursoCreate, capa: UploadFile) -> Cursos:
    """
    Cria um novo curso.
    """

    if capa.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(400, detail="O formato da capa anexada não correposponde aos permitidos")
    
    capa_bytes = await capa.read()

    db_curso = Cursos(
        nome=curso.nome,
        descricao=curso.descricao,
        capa=base64.b64encode(capa_bytes).decode(),
        capa_mime=capa.content_type
    )
    
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    
    return db_curso


async def get_curso(db: Session, curso_id: int) -> Cursos:
    """
    Busca um curso pelo ID
    """
    curso = db.query(Cursos).filter(Cursos.id == curso_id).first()
    
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    
    return curso


async def get_cursos(db: Session, skip: int = 0, limit: int = 100) -> List[Cursos]:
    """
    Busca todos os cursos com paginação
    """
    return db.query(Cursos).offset(skip).limit(limit).all()


async def update_curso(db: Session, curso_id: int, curso_data: CursoUpdate, capa: UploadFile = None) -> Cursos:
    """
    Atualiza um curso existente, incluindo nova capa se fornecida.
    """
    curso = await get_curso(db, curso_id)
    
    update_data = curso_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(curso, key, value)

    if capa:
        if capa.content_type not in ["image/png", "image/jpeg"]:
            raise HTTPException(status_code=400, detail="Formato de imagem não suportado (use PNG ou JPEG)")

        conteudo_bytes = await capa.read()
        curso.capa = base64.b64encode(conteudo_bytes).decode()
        curso.capa_mime = capa.content_type

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


async def search_cursos_by_name(db: Session, name: str) -> List[Cursos]:
    """
    Busca cursos pelo nome.
    """
    # Busca cursos com nome que contém a string fornecida
    return db.query(Cursos).filter(
        or_(
            Cursos.nome.ilike(f"%{name}%"),
            Cursos.descricao.ilike(f"%{name}%")
        )
    ).all()