from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.databases import create_db_and_tables
from app.settings import SETTINGS_TYPE

from .authentication import views as auth
from .user import views as user


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


origins = [
    "http://localhost:5173",  # local frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # Indicate that cookies should be supported for cross-origin requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root(settings: SETTINGS_TYPE):
    return {"message": "Hello World", "token": settings.token}
