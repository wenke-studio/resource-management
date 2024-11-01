from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True)
    password: str | None = Field(default=None)
    username: str | None = Field(default=None)
