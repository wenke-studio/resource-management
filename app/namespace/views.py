from fastapi import APIRouter, HTTPException
from sqlmodel import select

from ..databases import SessionDep
from .models import Namespace

router = APIRouter(prefix="/namespaces", tags=["namespaces"])


@router.post("/")
def create_namespace(namespace: Namespace, session: SessionDep):
    session.add(namespace)
    session.commit()
    return {"message": "Namespace created successfully"}


@router.get("/")
def read_namespaces(session: SessionDep):
    return session.exec(select(Namespace)).all()


@router.get("/{id}")
def retrieve_namespace(id: str, session: SessionDep):
    namespace = session.exec(select(Namespace).where(Namespace.id == id)).first()
    if not namespace:
        raise HTTPException(status_code=404, detail="Namespace not found")
    return namespace


@router.patch("/{id}")
def update_namespace(id: str, namespace: Namespace, session: SessionDep):
    session.exec(select(Namespace).where(Namespace.id == id)).update(namespace)
    session.commit()
    return {"message": "Namespace updated successfully"}


@router.delete("/{id}")
def delete_namespace(id: str, session: SessionDep):
    session.exec(select(Namespace).where(Namespace.id == id)).delete()
    session.commit()
    return {"message": "Namespace deleted successfully"}
