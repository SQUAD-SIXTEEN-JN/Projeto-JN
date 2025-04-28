import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from fastapi import HTTPException, status
from jose import jwt, ExpiredSignatureError, JWTError

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60

def criar_jwt(matricula: int):
    """
    Faz a criação do jwt retornando o token
    """
    exp = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    payload = {
        "sub": str(matricula),
        "exp": exp
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return token


def verificar_jwt(token: str):
    """
    Valida e decodifica o jwt, retornando a matrícula do usuário em caso de sucesso
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )