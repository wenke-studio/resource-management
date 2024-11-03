from typing import Annotated

from fastapi import Cookie, Depends

from ..settings import SettingsDep
from ..user.models import User
from . import clerk

ANONYMOUS_USER = User(id="-1", email="anonymous@email.com", username="anonymous")


def get_user(
    settings: SettingsDep,
    __session: Annotated[str | None, Cookie()] = None,
) -> User:
    if __session is None:
        return ANONYMOUS_USER

    try:
        token = clerk.decode_session_token(settings.clerk_secret_key, __session)
        user = clerk.get_user(settings.clerk_secret_key, token.sub)
        if user:
            return user
        return ANONYMOUS_USER
    except Exception:  # todo: enhance excepts
        return ANONYMOUS_USER


UserDep = Annotated[User, Depends(get_user)]
