from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.user.models import User


class NamespaceMember(SQLModel, table=True):
    namespace_id: str = Field(
        default=None, foreign_key="namespace.id", primary_key=True
    )
    user_id: str = Field(default=None, foreign_key="user.id", primary_key=True)


class Namespace(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    name: str

    members: list["User"] = Relationship(
        back_populates="namespaces", link_model=NamespaceMember
    )
