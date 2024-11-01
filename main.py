from functools import lru_cache
from typing import Annotated, Union

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from config import Settings

app = FastAPI()


@lru_cache
def get_settings():
    return Settings(token="hello world")


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
def read_root(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "Hello": "World",
        "settings": settings.token,
    }


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
