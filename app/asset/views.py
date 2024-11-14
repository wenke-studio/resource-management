from pathlib import Path

import magic
from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile, status
from sqlmodel import select

from ..databases import SessionDep
from .models import Asset

router = APIRouter(
    prefix="/assets",
    tags=["assets"],
)


def file_storage(filename: str, content: bytes):
    # todo: use cloud storage instead of local file system

    path = Path(__file__).parent / "files" / filename.strip()
    path.parent.mkdir(exist_ok=True, parents=True)
    with open(path, "wb") as fw:
        fw.write(content)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Asset)
async def create_asset(
    upload_file: UploadFile, session: SessionDep, background_task: BackgroundTasks
):
    content = await upload_file.read()
    asset = Asset(
        filename=upload_file.filename,
        mime_type=magic.from_buffer(content, mime=True),
        size=upload_file.size,
    )
    session.add(asset)
    session.commit()
    session.refresh(asset)
    background_task.add_task(file_storage, asset.storage_path, content)
    return asset


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[Asset])
async def list_assets(session: SessionDep):
    return session.exec(select(Asset)).all()


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=Asset)
async def retrieve_asset(id: int, session: SessionDep):
    asset = session.exec(select(Asset).where(Asset.id == id)).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


# todo: define update method


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(id: int, session: SessionDep):
    asset = session.get(Asset, id)
    if asset:
        session.delete(asset)
        session.commit()
    return {"message": "Asset deleted"}
