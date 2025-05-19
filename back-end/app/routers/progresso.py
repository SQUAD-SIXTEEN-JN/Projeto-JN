from typing import List, Dict, Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.progresso import ProgressoCreate, ProgressoResponse, ProgressoUpdate, ProgressoWithCursoResponse
from app.services.progresso_service import (
    create_progresso,
    get_progressos,
    get_progressos_by_usuario,
    get_progresso_by_usuario_curso,
    get_progressos_by_usuario_with_cursos,
    update_progresso_by_usuario_curso,
    delete_progresso_by_usuario_curso
)

router = APIRouter()


@router.post("/", response_model=ProgressoResponse, status_code=201)
async def create_progresso_route(
    progresso: ProgressoCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo registro de progresso para um usuário em um curso.
    """
    return await create_progresso(db=db, progresso=progresso)


@router.get("/", response_model=List[ProgressoResponse])
async def read_progressos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Busca todos os progressos com paginação.
    """
    return await get_progressos(db=db, skip=skip, limit=limit)


@router.get("/usuario/{usuario_id}", response_model=List[ProgressoResponse])
async def read_progressos_by_usuario(
    usuario_id: int = Path(..., title="ID do usuário", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca todos os progressos de um usuário específico.
    """
    return await get_progressos_by_usuario(db=db, usuario_id=usuario_id)


@router.get("/usuario/{usuario_id}/detalhado", response_model=List[ProgressoWithCursoResponse])
async def read_progressos_by_usuario_with_cursos(
    usuario_id: int = Path(..., title="ID do usuário", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca todos os progressos de um usuário específico, incluindo informações dos cursos.
    """
    return await get_progressos_by_usuario_with_cursos(db=db, usuario_id=usuario_id)


@router.get("/usuario/{usuario_id}/curso/{curso_id}", response_model=Optional[ProgressoResponse])
async def read_progresso_by_usuario_curso(
    usuario_id: int = Path(..., title="ID do usuário", ge=1),
    curso_id: int = Path(..., title="ID do curso", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca um progresso específico pelo ID do usuário e ID do curso.
    """
    progresso = await get_progresso_by_usuario_curso(db=db, usuario_id=usuario_id, curso_id=curso_id)
    if not progresso:
        raise HTTPException(status_code=404, detail="Progresso não encontrado")
    return progresso


@router.patch("/usuario/{usuario_id}/curso/{curso_id}", response_model=ProgressoResponse)
async def update_progresso_by_usuario_curso_route(
    progresso_data: ProgressoUpdate,
    usuario_id: int = Path(..., title="ID do usuário", ge=1),
    curso_id: int = Path(..., title="ID do curso", ge=1),
    db: Session = Depends(get_db)
):
    """
    Atualiza um progresso para um usuário e curso específicos.
    """
    return await update_progresso_by_usuario_curso(
        db=db, 
        usuario_id=usuario_id, 
        curso_id=curso_id, 
        progresso_data=progresso_data
    )


@router.delete("/usuario/{usuario_id}/curso/{curso_id}", response_model=Dict[str, bool])
async def delete_progresso_by_usuario_curso_route(
    usuario_id: int = Path(..., title="ID do usuário", ge=1),
    curso_id: int = Path(..., title="ID do curso", ge=1),
    db: Session = Depends(get_db)
):
    """
    Remove um progresso específico pelo ID do usuário e ID do curso.
    """
    return await delete_progresso_by_usuario_curso(db=db, usuario_id=usuario_id, curso_id=curso_id)