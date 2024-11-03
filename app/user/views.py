from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..databases import SessionDep
from .models import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/")
async def create_user(user: User, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/")
async def read_users(session: SessionDep):
    return session.exec(select(User)).all()


@router.get("/{id}")
async def retrieve_user(id: str, session: SessionDep):
    user = session.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# @router.patch("/{id}")
# async def update_user(id: str, user: User, session: SessionDep):
#     session.exec(select(User).where(User.id == id)).update(user)
#     session.commit()
#     return user


@router.delete("/{id}")
async def delete_user(id: str, session: SessionDep):
    user = session.get(User, id)
    if user:
        session.delete(user)
        session.commit()
    return {"message": "User deleted"}
