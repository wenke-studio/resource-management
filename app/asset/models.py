from hashlib import sha256

from sqlmodel import Field, SQLModel


def format_filename(id: int, filename: str) -> str:
    fmt = f"{id}-{filename}"
    return sha256(fmt.encode()).hexdigest()


class Asset(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    filename: str
    mime_type: str
    size: int

    @property
    def storage_path(self) -> str:
        return f"{self.mime_type}/{format_filename(self.id, self.filename)}"
