from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from .config import Settings
from .routers import users

app = FastAPI()

app.include_router(users.router)


@lru_cache
def get_settings():
    return Settings(token="hello world")


@app.get("/")
async def root(settings: Annotated[Settings, Depends(get_settings)]):
    return {"message": "Hello World", "token": settings.token}
