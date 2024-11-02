from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

from app.namespace.models import NamespaceMember

if TYPE_CHECKING:
    from app.namespace.models import Namespace


class User(SQLModel, table=True):
    id: str | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    username: str | None = Field(default=None)

    namespaces: list["Namespace"] = Relationship(
        back_populates="members", link_model=NamespaceMember
    )
