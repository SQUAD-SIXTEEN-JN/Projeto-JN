from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.usuario import UsuarioCreate
from app.schemas.login import Login
from app.utils.password import hash_password, verify_password
from app.utils.jwt import criar_jwt
from app.database import get_db
from app.models.models import Usuario, Perfil

router = APIRouter()

@router.post("/register", summary="Registrar Usuário")
def register_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    """
    Registra um novo usuário.

    - Verifica se o usuário já existe.
    - Valida o perfil informado.
    - Criptografa a senha e registra o usuário no banco.

    Exceções:
    - HTTP 400: "Usuário já existe" se a matrícula já estiver cadastrada.
    - HTTP 400: "Não existe o perfil {perfil}" se o perfil não for encontrado.

    Retorna:
    - Mensagem de sucesso se o usuário for registrado com sucesso.
    """

    # Verifica se o usuário já está cadastrado (busca pela existência da matrícula)
    existing_user = db.query(Usuario).filter(Usuario.matricula == user.matricula).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    # Verifica a existência do perfil e retorna seu id
    formatted_perfil = user.perfil.strip().lower()
    perfil_db = db.query(Perfil).filter(Perfil.nome == formatted_perfil).first()

    if not perfil_db:
        raise HTTPException(status_code=400, detail=f"Não existe o perfil {formatted_perfil.capitalize()}")
    
    # Cadastro do usuário
    hashed_senha = hash_password(user.senha)
    new_user = Usuario(
        matricula=user.matricula,
        nome=user.nome,
        senha_hash=hashed_senha,
        fk_perfil=perfil_db.id
    )
    db.add(new_user)
    db.commit()
    return {"message": "Usuário registrado com sucesso"}


@router.post("/login", summary="Login")
def login_user(login: Login, db: Session = Depends(get_db)):
    """
    Realiza o login do usuário.

    - Valida as credenciais (matrícula e senha).
    - Se for o primeiro acesso, altera o status.
    - Retorna um token JWT.

    Exceções:
    - HTTP 401: "Credenciais inválidas" se a matrícula ou senha forem incorretas.

    Retorna:
    - Token de acesso JWT.
    - Status de primeiro acesso (True/False).
    """

    # Verificando as credenciais (existência no banco e a validação da senha)
    user = db.query(Usuario).filter(Usuario.matricula == login.matricula).first()
    if not user or not verify_password(login.senha, user.senha_hash):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    
    # Realizando a modificação do parâmetro de primeiro acesso
    if user.primeiro_acesso:
        is_first_acess = True
        user.primeiro_acesso = False
        db.commit()
    else:
        is_first_acess = False
    
    token = criar_jwt(user.matricula)

    username = user.nome

    return {
        "username": username,
        "first_acess": is_first_acess,
        "access_token": token,
        "token_type": "bearer"
    }