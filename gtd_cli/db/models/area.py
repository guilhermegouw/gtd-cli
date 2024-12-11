from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base

class Area(Base):
    __tablename__ = "areas"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String)
    
    # Relationships
    projects: Mapped[List["Project"]] = relationship(
        back_populates="area",
        cascade="all, delete-orphan"
    )
    items: Mapped[List["Item"]] = relationship(
        back_populates="area",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Area {self.id}: {self.name}>"
