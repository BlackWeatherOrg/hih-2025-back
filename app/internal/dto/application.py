from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

from internal.core.types.application import ApplicationCategoryEnum


class ApplicationOut(BaseModel):
    id: int
    name: str
    rating: Optional[float] = None
    popularity: Optional[float] = None
    created_at: date
    editors_choice: Optional[bool] = None
    category: ApplicationCategoryEnum
    developer: Optional[str] = None
    age: Optional[str] = None
    description: Optional[str] = None
    downloads: Optional[str] = None
    apk_size: Optional[str] = None
    screenshots: list[str] = Field(default_factory=list)
    icon_link: Optional[str] = None
    fun_fact: Optional[str] = None
    apk_link: Optional[str] = None


class CreateApplicationDTO(BaseModel):
    name: str
    rating: Optional[float] = None
    popularity: Optional[float] = None
    editors_choice: Optional[bool] = None
    category: ApplicationCategoryEnum
    developer: Optional[str] = None
    age: Optional[str] = None
    description: Optional[str] = None
    downloads: Optional[str] = None
    apk_size: Optional[str] = None
    screenshots: list[str] = Field(default_factory=list)
    icon_link: Optional[str] = None
    fun_fact: Optional[str] = None
    apk_link: Optional[str] = None
    created_at: Optional[date] = None


class UpdateApplicationDTO(BaseModel):
    name: Optional[str] = None
    rating: Optional[float] = None
    popularity: Optional[float] = None
    editors_choice: Optional[bool] = None
    category: Optional[ApplicationCategoryEnum] = None
    developer: Optional[str] = None
    age: Optional[str] = None
    description: Optional[str] = None
    downloads: Optional[str] = None
    apk_size: Optional[str] = None
    screenshots: Optional[list[str]] = None
    icon_link: Optional[str] = None
    fun_fact: Optional[str] = None
    apk_link: Optional[str] = None
    created_at: Optional[date] = None


class GetApplicationDTO(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    category: Optional[ApplicationCategoryEnum] = None
    developer: Optional[str] = None
    editors_choice: Optional[bool] = None
    return_in_order: bool = True

