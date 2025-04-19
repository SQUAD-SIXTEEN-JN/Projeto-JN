import jwt
from datetime import datetime, timedelta

SECRET_KEY = "seu_segredo_muito_forte_aqui"  # coloque no .env depois
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60

def criar_jwt(matricula: int):
    exp = datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    payload = {
        "sub": str(matricula),
        "exp": exp
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verificar_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")
