from sqlalchemy.orm import Session
from app.models.models import Conteudo
from app.schemas.conteudo import ConteudoCreate, ConteudoUpdate

def criar_conteudo(db: Session, conteudo: ConteudoCreate):
    novo = Conteudo(**conteudo.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo

def listar_conteudos(db: Session):
    return db.query(Conteudo).all()

def buscar_conteudo(db: Session, video_id: int):
    return db.query(Conteudo).filter(Conteudo.id == video_id).first()

def atualizar_video(db: Session, video_id: int, dados: ConteudoUpdate):
    video = buscar_conteudo(db, video_id)
    if video:
        for attr, value in dados.dict().items():
            setattr(video, attr, value)
        db.commit()
        db.refresh(video)
    return video

def deletar_conteudo(db: Session, video_id: int):
    video = buscar_conteudo(db, video_id)
    if video:
        db.delete(video)
        db.commit()
    return video
