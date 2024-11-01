import logging
from functools import lru_cache

import jwt
from clerk_backend_api import Clerk, models
from pydantic import BaseModel

logger = logging.getLogger(__name__)


@lru_cache
def get_clerk(bearer_auth: str) -> Clerk:
    return Clerk(bearer_auth)


@lru_cache
def get_jwks(bearer_auth: str) -> models.Keys:
    clerk = get_clerk(bearer_auth)
    response = clerk.jwks.get()
    return response.keys[0]


class ClerkSessionToken(BaseModel):
    """Clerk session token

    NOTE: skip `actor` and `organization` claims for now

    ref: https://clerk.com/docs/backend-requests/resources/session-tokens
    """

    azp: str  # authorized party

    exp: int  # expiration time (RFC 7519)

    iat: int  # issued at (RFC 7519)

    iss: str  # issuer

    nbf: int  # not before (RFC 7519)

    sid: str  # session id - the id of the current session

    sub: str  # subject - the id of the current user of the session


def decode_session_token(
    clerk_secret_key: str, session_token: str
) -> ClerkSessionToken:
    key = get_jwks(clerk_secret_key)  # cache
    payload = jwt.decode(session_token, key.n, algorithms=[key.alg])
    return ClerkSessionToken(**payload)


def revoke_session(clerk_secret_key: str, session_id: str):
    clerk = get_clerk(clerk_secret_key)
    clerk.sessions.revoke(session_id=session_id)


def get_user(clerk_secret_key: str, user_id: str) -> models.User:
    clerk = get_clerk(clerk_secret_key)
    return clerk.users.get(user_id=user_id)
