from fastapi import FastAPI

from .routers import users
from .settings import SETTINGS_TYPE

app = FastAPI()

app.include_router(users.router)


@app.get("/")
async def root(settings: SETTINGS_TYPE):
    return {"message": "Hello World", "token": settings.token}
