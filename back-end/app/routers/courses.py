from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.curso import Curso
from app.utils.db import get_db
from app.schemas.curso import Curso as CursoSchema

router = APIRouter()

@router.get("/cursos/{perfil_id}", response_model=List[CursoSchema])
def get_cursos_por_perfil(perfil_id: int, db: Session = Depends(get_db)):
    cursos = db.query(Curso).filter(Curso.fk_perfil == perfil_id).all()
    if not cursos:
        raise HTTPException(status_code=404, detail="Nenhum curso encontrado para este perfil")
    return cursos