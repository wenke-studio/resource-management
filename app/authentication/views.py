from typing import Annotated, Union

from clerk_backend_api.models import ClerkErrors, SDKError
from fastapi import APIRouter, Cookie, HTTPException
from jwt.exceptions import InvalidTokenError

from ..databases import SessionDep
from ..settings import SettingsDep
from ..user.models import User
from . import clerk

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/login")
async def login(
    settings: SettingsDep,
    session: SessionDep,
    __session: Annotated[Union[str, None], Cookie()] = None,
):
    try:
        token = clerk.decode_session_token(settings.clerk_secret_key, __session)
        user = session.get(User, token.sub)
        if not user:
            clerk_user = clerk.get_user(settings.clerk_secret_key, token.sub)
            session.add(
                User(
                    id=clerk_user.id,
                    email=clerk_user.email_addresses[0].email_address,
                    password=None,
                    username=clerk_user.username,
                )
            )
            session.commit()
        return {"message": "user logged in"}
    except (InvalidTokenError, SDKError, ClerkErrors):
        raise HTTPException(status_code=401, detail="Invalid session token")


@router.get("/logout")
async def logout(
    settings: SettingsDep,
    __session: Annotated[Union[str, None], Cookie()] = None,
):
    try:
        clerk.revoke_session(settings.clerk_secret_key, __session)
        return {"message": "logged out"}
    except (ClerkErrors, SDKError):
        raise HTTPException(status_code=401, detail="Invalid session token")
