from typing import List, Dict, Optional, Union, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from fastapi import HTTPException

from app.models.models import Progressos, Usuario, Cursos
from app.schemas.progresso import ProgressoCreate, ProgressoUpdate


async def create_progresso(db: Session, progresso: ProgressoCreate) -> Progressos:
    """
    Cria um novo registro de progresso.
    """
    # Verificar se o usuário existe
    usuario = db.query(Usuario).filter(Usuario.matricula == progresso.fk_usuario).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário com ID {progresso.fk_usuario} não encontrado"
        )
    
    # Verificar se o curso existe
    curso = db.query(Cursos).filter(Cursos.id == progresso.fk_curso).first()
    if not curso:
        raise HTTPException(
            status_code=404,
            detail=f"Curso com ID {progresso.fk_curso} não encontrado"
        )
    
    # Verificar se já existe um progresso para este usuário e curso
    existing = db.query(Progressos).filter(
        and_(
            Progressos.fk_usuario == progresso.fk_usuario,
            Progressos.fk_curso == progresso.fk_curso
        )
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Já existe um registro de progresso para este usuário e curso"
        )
    
    db_progresso = Progressos(
        progresso=progresso.progresso,
        fk_usuario=progresso.fk_usuario,
        fk_curso=progresso.fk_curso
    )
    
    db.add(db_progresso)
    db.commit()
    db.refresh(db_progresso)
    
    return db_progresso


async def get_progresso_by_usuario_curso(db: Session, usuario_id: int, curso_id: int) -> Optional[Progressos]:
    """
    Busca um progresso pelo ID do usuário e ID do curso.
    """
    # Verificar se o usuário existe
    usuario = db.query(Usuario).filter(Usuario.matricula == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário com ID {usuario_id} não encontrado"
        )
    
    # Verificar se o curso existe
    curso = db.query(Cursos).filter(Cursos.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=404,
            detail=f"Curso com ID {curso_id} não encontrado"
        )
    
    progresso = db.query(Progressos).filter(
        and_(
            Progressos.fk_usuario == usuario_id,
            Progressos.fk_curso == curso_id
        )
    ).first()
    
    return progresso


async def get_progressos(db: Session, skip: int = 0, limit: int = 100) -> List[Progressos]:
    """
    Busca todos os progressos com paginação.
    """
    return db.query(Progressos).offset(skip).limit(limit).all()


async def get_progressos_by_usuario(db: Session, usuario_id: int) -> List[Progressos]:
    """
    Busca todos os progressos de um usuário específico.
    """
    # Verificar se o usuário existe
    usuario = db.query(Usuario).filter(Usuario.matricula == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário com ID {usuario_id} não encontrado"
        )
    
    return db.query(Progressos).filter(Progressos.fk_usuario == usuario_id).all()


async def get_progressos_by_usuario_with_cursos(db: Session, usuario_id: int) -> List[Dict[str, Any]]:
    """
    Busca todos os progressos de um usuário específico, incluindo informações dos cursos.
    """
    # Verificar se o usuário existe
    usuario = db.query(Usuario).filter(Usuario.matricula == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário com ID {usuario_id} não encontrado"
        )
    
    # Buscar progressos com join das informações do curso
    progressos = db.query(Progressos).join(
        Cursos, Progressos.fk_curso == Cursos.id
    ).filter(
        Progressos.fk_usuario == usuario_id
    ).add_entity(Cursos).all()
    
    # Formatar a resposta com informações do curso
    resultado = []
    for progresso, curso in progressos:
        resultado.append({
            "id": progresso.id,
            "progresso": progresso.progresso,
            "fk_usuario": progresso.fk_usuario,
            "curso": {
                "id": curso.id,
                "nome": curso.nome,
                "descricao": curso.descricao
            }
        })
    
    return resultado


async def get_progressos_by_curso(db: Session, curso_id: int) -> List[Progressos]:
    """
    Busca todos os progressos de um curso específico.
    """
    # Verificar se o curso existe
    curso = db.query(Cursos).filter(Cursos.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=404,
            detail=f"Curso com ID {curso_id} não encontrado"
        )
    
    return db.query(Progressos).filter(Progressos.fk_curso == curso_id).all()


async def update_progresso_by_usuario_curso(
    db: Session, 
    usuario_id: int, 
    curso_id: int, 
    progresso_data: ProgressoUpdate
) -> Union[Progressos, Dict[str, str]]:
    """
    Atualiza ou cria um progresso para um usuário e curso específicos.
    """
    # Verificar se o usuário existe
    usuario = db.query(Usuario).filter(Usuario.matricula == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário com ID {usuario_id} não encontrado"
        )
    
    # Verificar se o curso existe
    curso = db.query(Cursos).filter(Cursos.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=404,
            detail=f"Curso com ID {curso_id} não encontrado"
        )
    
    progresso = await get_progresso_by_usuario_curso(db, usuario_id, curso_id)
    
    if not progresso:
        # Se não existir, cria um novo registro
        novo_progresso = ProgressoCreate(
            progresso=progresso_data.progresso or 0,
            fk_usuario=usuario_id,
            fk_curso=curso_id
        )
        return await create_progresso(db, novo_progresso)
    
    # Atualiza apenas os campos fornecidos
    update_data = progresso_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(progresso, key, value)
    
    db.commit()
    db.refresh(progresso)
    
    return progresso


async def delete_progresso_by_usuario_curso(db: Session, usuario_id: int, curso_id: int) -> Dict[str, bool]:
    """
    Remove um progresso específico pelo ID do usuário e ID do curso.
    """
    # Verificar se o usuário existe
    usuario = db.query(Usuario).filter(Usuario.matricula == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=404,
            detail=f"Usuário com ID {usuario_id} não encontrado"
        )
    
    # Verificar se o curso existe
    curso = db.query(Cursos).filter(Cursos.id == curso_id).first()
    if not curso:
        raise HTTPException(
            status_code=404,
            detail=f"Curso com ID {curso_id} não encontrado"
        )
    
    progresso = await get_progresso_by_usuario_curso(db, usuario_id, curso_id)
    
    if not progresso:
        raise HTTPException(status_code=404, detail="Progresso não encontrado")
    
    db.delete(progresso)
    db.commit()
    
    return {"success": True}