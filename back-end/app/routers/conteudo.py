from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.conteudo import ConteudoCreate, ConteudoResponse, ConteudoUpdate
from app.services import conteudo_service

router = APIRouter(prefix="/videos", tags=["Videos"])

@router.post("/", response_model=ConteudoResponse)
def criar(video: ConteudoCreate, db: Session = Depends(get_db)):
    return conteudo_service.criar_conteudo(db, video)

@router.get("/", response_model=list[ConteudoResponse])
def listar(db: Session = Depends(get_db)):
    return conteudo_service.listar_conteudos(db)

@router.get("/{video_id}", response_model=ConteudoResponse)
def buscar(video_id: int, db: Session = Depends(get_db)):
    video = conteudo_service.buscar_conteudo(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    return video

@router.put("/{video_id}", response_model=ConteudoResponse)
def atualizar(video_id: int, dados: ConteudoUpdate, db: Session = Depends(get_db)):
    video = conteudo_service.atualizar_video(db, video_id, dados)
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    return video

@router.delete("/{video_id}")
def deletar(video_id: int, db: Session = Depends(get_db)):
    video = conteudo_service.deletar_conteudo(db, video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não encontrado")
    return {"detail": "Vídeo deletado com sucesso"}
