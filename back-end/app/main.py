from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.menu import router as menu_router
from app.routers.perfil import router as perfil_router
from app.routers.permissoes import router as permissoes_router
from app.routers.curso import router as curso_router
from app.routers.modulo import router as modulo_router

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="SQUAD SIXTEEN - JN",
    version="v1"
    )

app.include_router(auth_router, prefix=f"/{app.version}/auth", tags=["Autenticação"])
app.include_router(menu_router, prefix=f"/{app.version}/menu", tags=["Menu"]) 
app.include_router(perfil_router, prefix=f"/{app.version}/perfil", tags=["Perfil"])
app.include_router(permissoes_router, prefix=f"/{app.version}/permissoes", tags=["Permissões dos Menus"])
app.include_router(curso_router, prefix=f"/{app.version}/curso", tags=["Cursos"])
app.include_router(modulo_router, prefix=f"/{app.version}/modulo", tags=["Módulos dos Cursos"])
