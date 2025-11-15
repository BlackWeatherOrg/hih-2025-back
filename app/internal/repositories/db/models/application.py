from datetime import date

from sqlalchemy import Boolean, Enum, Float, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import text as sa_text

from internal.core.types.application import ApplicationCategoryEnum
from internal.dto.application import ApplicationOut
from internal.repositories.db.models.base import BaseOrm


class Application(BaseOrm):
    __tablename__ = 'applications'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    rating: Mapped[float | None] = mapped_column(Float, nullable=True)
    popularity: Mapped[float] = mapped_column(Float, nullable=True)
    editors_choice: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    category: Mapped[ApplicationCategoryEnum] = mapped_column(Enum(ApplicationCategoryEnum), nullable=False)
    developer: Mapped[str] = mapped_column(String(255), nullable=True)
    age: Mapped[str] = mapped_column(String(32), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    downloads: Mapped[str] = mapped_column(Text, nullable=True)
    apk_size: Mapped[str] = mapped_column(Text, nullable=True)
    screenshots: Mapped[list[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        server_default=sa_text('ARRAY[]::text[]'),
        default=list,
    )
    icon_link: Mapped[str] = mapped_column(String(512), nullable=True)
    fun_fact: Mapped[str | None] = mapped_column(Text, nullable=True)
    apk_link: Mapped[str] = mapped_column(String(512), nullable=True)

    created_at: Mapped[date] = mapped_column(server_default=func.now(), nullable=False)

    def to_dto(self) -> ApplicationOut:
        return ApplicationOut(
            id=self.id,
            name=self.name,
            rating=self.rating,
            popularity=self.popularity,
            created_at=self.created_at,
            editors_choice=self.editors_choice,
            category=self.category,
            developer=self.developer,
            age=self.age,
            description=self.description,
            downloads=self.downloads,
            apk_size=self.apk_size,
            screenshots=self.screenshots or [],
            icon_link=self.icon_link,
            fun_fact=self.fun_fact,
            apk_link=self.apk_link,
        )

