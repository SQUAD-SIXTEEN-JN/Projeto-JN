from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.menu import router as menu_router

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="SQUAD SIXTEEN - JN",
    version="v1"
    )

app.include_router(auth_router, prefix=f"/{app.version}/auth", tags=["Autenticação"])
app.include_router(menu_router, prefix=f"/{app.version}/menu", tags=["Menus"])
