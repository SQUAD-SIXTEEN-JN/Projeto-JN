import os
from fastapi import FastAPI, Depends, HTTPException, Security, APIRouter
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security.oauth2 import OAuth2
from jose import JWTError, jwt
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from dotenv import load_dotenv
import requests
from pydantic import BaseModel
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Carregar variáveis de ambiente
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

# Configuração do banco de dados
DATABASE_URL = os.getenv("NEON_DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL não está definido no .env!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configurações do Auth0
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "myapp.auth0.com")
API_AUDIENCE = os.getenv("API_AUDIENCE", "myapi")
ALGORITHM = "RS256"
JWKS_URL = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_public_key():
    try:
        response = requests.get(JWKS_URL)
        jwks = response.json()
        return jwks["keys"][0]
    except Exception:
        raise ValueError("Erro ao obter a chave pública do Auth0")

PUBLIC_KEY = get_public_key()

class OAuth2PasswordBearerWithBearer(OAuth2):
    def __init__(self, tokenUrl: str):
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl})
        super().__init__(flows=flows)

oauth2_scheme = OAuth2PasswordBearerWithBearer(tokenUrl="/api/auth/login")

class Perfil(Base):
    __tablename__ = "perfis"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(50), nullable=False)

class Usuario(Base):
    __tablename__ = "usuarios"
    matricula = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    senha_hash = Column(String(255), nullable=False)
    primeiro_acesso = Column(Boolean, default=True)
    fk_perfil = Column(Integer, ForeignKey("perfis.id"), nullable=False)

class UsuarioCreate(BaseModel):
    nome: str
    matricula: int
    senha: str  # Recebe a senha em texto plano
    fk_perfil: int

class Login(BaseModel):
    matricula: int
    senha: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

async def verify_token(token: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM], audience=API_AUDIENCE)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

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
        senha_hash=hashed_senha,  # Agora corretamente nomeado
        fk_perfil=user.fk_perfil
    )
    db.add(new_user)
    db.commit()
    return {"message": "Usuário registrado com sucesso"}

@router.post("/auth/login")
def login_user(login: Login, db: Session = Depends(get_db)):
    matricula = login.matricula
    senha = login.senha

    if not matricula or not senha:
        raise HTTPException(status_code=400, detail="Matrícula e senha são obrigatórios")

    user = db.query(Usuario).filter(Usuario.matricula == matricula).first()
    if not user or not verify_password(senha, user.senha_hash):
        raise HTTPException(status_code=400, detail="Matrícula ou senha incorretas")

    access_token = create_access_token({"sub": str(user.matricula)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, PUBLIC_KEY, algorithms=[ALGORITHM], audience=API_AUDIENCE)
        matricula = int(payload.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    user = db.query(Usuario).filter(Usuario.matricula == matricula).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {"matricula": user.matricula, "nome": user.nome, "primeiro_acesso": user.primeiro_acesso}

app = FastAPI()
app.include_router(router, prefix="/api")
Base.metadata.create_all(bind=engine)
