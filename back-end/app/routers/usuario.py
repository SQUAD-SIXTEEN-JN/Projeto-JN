from typing import List, Dict, Union
from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.usuario import UsuarioResponse, UsuarioUpdate
from app.services.usuario_service import (
    get_usuario,
    get_usuarios,
    update_usuario,
    delete_usuario
)

router = APIRouter()


@router.get("/", response_model=List[Dict])
async def read_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Lista todos os usuários
    """
    return await get_usuarios(db=db, skip=skip, limit=limit)


@router.get("/{matricula}", response_model=Dict)
async def read_usuario(
    matricula: int = Path(..., title="Matrícula do usuário", ge=1),
    db: Session = Depends(get_db)
):
    """
    Busca um usuário pela matrícula
    """
    return await get_usuario(db=db, matricula=matricula)


@router.patch("/{matricula}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_data: UsuarioUpdate,
    matricula: int = Path(..., title="Matrícula do usuário", ge=1),
    db: Session = Depends(get_db)
):
    """
    Atualiza um usuário existente.
    """
    return await update_usuario(db=db, matricula=matricula, usuario_data=usuario_data)


@router.delete("/{matricula}", response_model=Dict[str, bool])
async def delete_usuario_route(
    matricula: int = Path(..., title="Matrícula do usuário", ge=1),
    db: Session = Depends(get_db)
):
    """
    Remove um usuário do banco de dados.
    """
    return await delete_usuario(db=db, matricula=matricula)