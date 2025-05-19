from typing import List, Dict
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.curso import CursoCreate, CursoResponse, CursoUpdate
from app.services.curso_service import (
    create_curso,
    get_curso,
    get_cursos,
    update_curso,
    delete_curso,
    search_cursos_by_name
)

router = APIRouter()

@router.post("/", response_model=CursoResponse, status_code=201)
async def create_curso_route(
    curso: CursoCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo curso.
    """
    return await create_curso(db=db, curso=curso)

@router.get("/{curso_id}", response_model=CursoResponse)
async def read_curso(
    curso_id: int = Path(..., title="ID do curso", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca um curso pelo ID.
    """
    return await get_curso(db=db, curso_id=curso_id)

@router.get("/", response_model=List[CursoResponse])
async def read_cursos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Busca todos os cursos com paginação.
    """
    return await get_cursos(db=db, skip=skip, limit=limit)

@router.patch("/{curso_id}", response_model=CursoResponse)
async def update_curso_route(
    curso_data: CursoUpdate,
    curso_id: int = Path(..., title="ID do curso", ge=1),
    db: Session = Depends(get_db)
):
    """
    Atualiza um curso existente.
    """
    return await update_curso(db=db, curso_id=curso_id, curso_data=curso_data)

@router.delete("/{curso_id}", response_model=Dict[str, bool])
async def delete_curso_route(
    curso_id: int = Path(..., title="ID do curso", ge=1),
    db: Session = Depends(get_db)
):
    """
    Remove um curso do banco de dados.
    """
    return await delete_curso(db=db, curso_id=curso_id)

@router.get("/search/", response_model=List[CursoResponse])
async def search_cursos(
    name: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """
    Busca cursos pelo nome.
    """
    return await search_cursos_by_name(db=db, name=name)