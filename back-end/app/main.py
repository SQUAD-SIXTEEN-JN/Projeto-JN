from fastapi import FastAPI
from app.routers import auth  # Importando o roteador de autenticação
from app.models import Base
from app.utils.db import engine
from dotenv import load_dotenv
from app.routers import courses
load_dotenv()

app = FastAPI()

app.include_router(auth.router, prefix="/api")  # Incluindo o roteador de autenticação
app.include_router(courses.router, prefix="/api")

Base.metadata.create_all(bind=engine)
