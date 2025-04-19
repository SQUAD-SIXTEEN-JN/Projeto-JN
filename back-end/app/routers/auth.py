from fastapi import APIRouter, Depends, HTTPException
from app.schemas.usuario import UsuarioCreate
from app.schemas.login import Login
from app.services.password import hash_password, verify_password
from app.utils.jwt import criar_jwt
from app.utils.db import get_db
from app.models.usuario import Usuario
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/auth/register")
def register_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Usuario).filter(Usuario.matricula == user.matricula).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    hashed_senha = hash_password(user.senha)  # Gerar o hash da senha antes de salvar
    new_user = Usuario(
        matricula=user.matricula,
        nome=user.nome,
        senha_hash=hashed_senha,
        fk_perfil=user.fk_perfil
    )
    db.add(new_user)
    db.commit()
    return {"message": "Usuário registrado com sucesso"}

@router.post("/auth/login")
def login_user(login: Login, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.matricula == login.matricula).first()
    if not user or not verify_password(login.senha, user.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = criar_jwt(user.matricula)
    return {
        "access_token": token,
        "token_type": "bearer"
    }