from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..authentication.dependencies import UserDep
from ..databases import SessionDep
from .models import Namespace

router = APIRouter(prefix="/namespaces", tags=["namespaces"])


@router.post("/")
def create_namespace(
    namespace: Namespace,
    session: SessionDep,
    user: UserDep,
):
    if user.id == "-1":
        raise HTTPException(status_code=401, detail="Unauthorized")

    namespace.members.append(user)
    session.add(namespace)
    session.commit()
    session.refresh(namespace)
    return namespace


@router.get("/")
def read_namespaces(session: SessionDep, user: UserDep):
    if user.id == "-1":
        raise HTTPException(status_code=401, detail="Unauthorized")

    return user.namespaces


@router.get("/{id}")
def retrieve_namespace(id: str, session: SessionDep, user: UserDep):
    if user.id == "-1":
        raise HTTPException(status_code=401, detail="Unauthorized")

    statement = select(Namespace).where(
        Namespace.id == id,
        Namespace.members.contains(user),
    )
    namespace = session.exec(statement).first()
    if not namespace:
        raise HTTPException(status_code=404, detail="Namespace not found")
    return namespace


# @router.patch("/{id}")
# def update_namespace(id: str, namespace: Namespace, session: SessionDep):
#     session.exec(select(Namespace).where(Namespace.id == id)).update(namespace)
#     session.commit()
#     return {"message": "Namespace updated successfully"}


@router.delete("/{id}")
def delete_namespace(id: str, session: SessionDep, user: UserDep):
    if user.id == "-1":
        raise HTTPException(status_code=401, detail="Unauthorized")

    statement = select(Namespace).where(
        Namespace.id == id,
        Namespace.members.contains(user),
    )
    namespace = session.exec(statement).first()
    if not namespace:
        raise HTTPException(status_code=404, detail="Namespace not found")

    session.delete(namespace)
    session.commit()
    return {"message": "Namespace deleted successfully"}
