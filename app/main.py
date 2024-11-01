from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI

from .routers import users
from .settings import Settings

app = FastAPI()

app.include_router(users.router)


@lru_cache
def get_settings():
    return Settings()


@app.get("/")
async def root(settings: Annotated[Settings, Depends(get_settings)]):
    return {"message": "Hello World", "token": settings.token}
