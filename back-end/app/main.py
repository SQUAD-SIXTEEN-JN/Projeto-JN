from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import router as auth_router
from app.routers.menu import router as menu_router
from app.routers.perfil import router as perfil_router
from app.routers.permissoes import router as permissoes_router
from app.routers.curso import router as curso_router
from app.routers.modulo import router as modulo_router
from app.routers.progresso import router  as progresso_router
from app.routers.usuario import router as usuario_router
from app.routers.conteudo import router as conteudo_router

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="SQUAD SIXTEEN - JN",
    version="v1"
    )

# ====================================================================
# ============== INÍCIO DA CONFIGURAÇÃO DE CORS ======================
# ====================================================================

# Lista de origens permitidas (domínios do front-end)
origins = [
    "http://localhost",      # Comum para desenvolvimento local
    "http://localhost:3000", # Comum para apps React
    "http://localhost:8080", # Outra porta de desenvolvimento comum
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True, # Necessário para enviar cookies/tokens de autenticação
    allow_methods=["*"],    # Permite todos os métodos: GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],    # Permite todos os cabeçalhos
)

# ====================================================================
# ================== FIM DA CONFIGURAÇÃO DE CORS =====================
# ====================================================================

app.include_router(auth_router, prefix=f"/{app.version}/auth", tags=["Autenticação"])
app.include_router(usuario_router, prefix=f"/{app.version}/usuario", tags=["Usuário"])
app.include_router(menu_router, prefix=f"/{app.version}/menu", tags=["Menu"]) 
app.include_router(perfil_router, prefix=f"/{app.version}/perfil", tags=["Perfil"])
app.include_router(permissoes_router, prefix=f"/{app.version}/permissoes", tags=["Permissões dos Menus"])
app.include_router(curso_router, prefix=f"/{app.version}/curso", tags=["Cursos"])
app.include_router(progresso_router, prefix=f"/{app.version}/progresso", tags=["Progresso dos Cursos"])
app.include_router(modulo_router, prefix=f"/{app.version}/modulo", tags=["Módulos dos Cursos"])
app.include_router(conteudo_router, prefix=f"/{app.version}/conteudo", tags=["Conteúdos"])