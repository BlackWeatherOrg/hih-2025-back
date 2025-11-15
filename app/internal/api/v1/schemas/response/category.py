from pydantic import BaseModel


class CategoriesOut(BaseModel):
    categories: list[str]
