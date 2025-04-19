from fastapi import FastAPI
from app.routers import auth  # Importando o roteador de autenticação
from app.models import Base
from app.utils.db import engine
from dotenv import load_dotenv
load_dotenv()

import os
print("DOMÍNIO:", os.getenv("AUTH0_DOMAIN"))


app = FastAPI()

app.include_router(auth.router, prefix="/api")  # Incluindo o roteador de autenticação

# Criação das tabelas no banco de dados
Base.metadata.create_all(bind=engine)
