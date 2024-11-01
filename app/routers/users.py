from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {"description": "Not found"},
    },
)


@router.get("/", tags=["users"])
async def read_users():
    return [
        {"username": "foo"},
        {"username": "bar"},
    ]


@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "current-user"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    if username in ["foo", "bar"]:
        return {"username": username}
    raise HTTPException(status_code=404, detail="User not found")
