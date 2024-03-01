from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, RootModel


class ProductLesson(BaseModel):
    id: UUID
    name: str
    price: float
    starting_date: datetime
    lesson_number: int


class ListProductLesson(RootModel):
    root: list[ProductLesson]