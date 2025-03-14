from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import EmailStr

from firebase.config import auth
from schemas.auth import UserRegister, Token


router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Função que verifica o token"""
    try:
        user = auth.get_account_info(token)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/register", response_model=Token)
async def register_user(user_data: UserRegister):
    """Rota para cadastrar um usuário"""
    try:
        user = auth.create_user_with_email_and_password(
            user_data.email, 
            user_data.password
        )
        
        return {
            "access_token": user["idToken"],
            "token_type": "bearer",
            "user_id": user["localId"],
            "refresh_token": user["refreshToken"]
        }
    except Exception as e:
        error_message = str(e)
        if "EMAIL_EXISTS" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está em uso"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Rota para executar o login"""
    try:
        user = auth.sign_in_with_email_and_password(
            form_data.username,
            form_data.password
        )
        
        return {
            "access_token": user["idToken"],
            "token_type": "bearer",
            "user_id": user["localId"],
            "refresh_token": user["refreshToken"]
        }
    except Exception as e:
        error_message = str(e)
        if "INVALID_PASSWORD" in error_message:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais incorretas",
                headers={"WWW-Authenticate": "Bearer"},
            )
        elif "EMAIL_NOT_FOUND" in error_message:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error_message,
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/refresh-token", response_model=Token)
async def refresh_token(refresh_token: str):
    """Rota para renovar o token"""
    try:
        user = auth.refresh(refresh_token)
        return {
            "access_token": user["idToken"],
            "token_type": "bearer",
            "user_id": user["userId"],
            "refresh_token": user["refreshToken"]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Não foi possível renovar o token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    

@router.post("/reset-password")
async def reset_password(email: EmailStr):
    """Rota para enviar link de redefinição de senha"""
    try:
        auth.send_password_reset_email(email)
        return {"message": "Email de redefinição de senha enviado com sucesso"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível enviar o email de redefinição de senha"
        )
    