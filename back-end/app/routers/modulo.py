from typing import List, Dict
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.modulo import ModuloCreate, ModuloResponse, ModuloUpdate, ModuloWithCursoResponse
from app.services.modulo_service import (
    create_modulo,
    get_modulo,
    get_modulos,
    update_modulo,
    delete_modulo,
    search_modulos_by_name,
    get_modulos_by_curso
)

router = APIRouter()

@router.post("/", response_model=ModuloResponse, status_code=201)
async def create_modulo_route(
    modulo: ModuloCreate,
    db: Session = Depends(get_db)
):
    """
    Cria um novo módulo.
    """
    return await create_modulo(db=db, modulo=modulo)

@router.get("/{modulo_id}", response_model=ModuloWithCursoResponse)
async def read_modulo(
    modulo_id: int = Path(..., title="ID do módulo", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca um módulo pelo ID.
    """
    return await get_modulo(db=db, modulo_id=modulo_id)

@router.get("/", response_model=List[ModuloResponse])
async def read_modulos(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Busca todos os módulos com paginação.
    """
    return await get_modulos(db=db, skip=skip, limit=limit)

@router.patch("/{modulo_id}", response_model=ModuloResponse)
async def update_modulo_route(
    modulo_data: ModuloUpdate,
    modulo_id: int = Path(..., title="ID do módulo", ge=1),
    db: Session = Depends(get_db)
):
    """
    Atualiza um módulo existente.
    """
    return await update_modulo(db=db, modulo_id=modulo_id, modulo_data=modulo_data)

@router.delete("/{modulo_id}", response_model=Dict[str, bool])
async def delete_modulo_route(
    modulo_id: int = Path(..., title="ID do módulo", ge=1),
    db: Session = Depends(get_db)
):
    """
    Remove um módulo do banco de dados.
    """
    return await delete_modulo(db=db, modulo_id=modulo_id)

@router.get("/search/", response_model=List[ModuloResponse])
async def search_modulos(
    name: str = Query(..., min_length=1),
    db: Session = Depends(get_db)
):
    """
    Busca módulos pelo nome.
    """
    return await search_modulos_by_name(db=db, name=name)

@router.get("/curso/{curso_id}", response_model=List[ModuloResponse])
async def read_modulos_by_curso(
    curso_id: int = Path(..., title="ID do curso", ge=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Busca todos os módulos de um curso específico.
    """
    return await get_modulos_by_curso(db=db, curso_id=curso_id, skip=skip, limit=limit)