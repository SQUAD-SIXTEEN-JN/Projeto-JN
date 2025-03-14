from fastapi import FastAPI

from routers.auth import router as auth_router

app = FastAPI(title="SQUAD SIXTEEN - JN ")
app.include_router(auth_router)