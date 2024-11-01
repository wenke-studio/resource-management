from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import users
from .settings import SETTINGS_TYPE

app = FastAPI()

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

app.include_router(users.router)


@app.get("/")
async def root(settings: SETTINGS_TYPE):
    return {"message": "Hello World", "token": settings.token}
