from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    """Valida a senha fornecida comparando a senha em texto claro com a senha hasheada"""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    """Gera um hash seguro para a senha fornecida utilizando o esquema bcrypt"""
    return pwd_context.hash(password)
