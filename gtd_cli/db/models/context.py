from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base

class Context(Base):
    __tablename__ = "contexts"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    
    # Relationships
    items: Mapped[List["Item"]] = relationship(
        back_populates="context",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Context {self.id}: {self.name}>"
