from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..base import Base
from enum import Enum

class ItemType(str, Enum):
    THOUGHT = "thought"
    TASK = "task"
    NOTE = "note"

class ItemStatus(str, Enum):
    INBOX = "inbox"
    NEXT_ACTION = "next_action"
    WAITING_FOR = "waiting_for"
    SOMEDAY_MAYBE = "someday_maybe"
    REFERENCE = "reference"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DROPPED = "dropped"

class EnergyLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Item(Base):
    __tablename__ = "items"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    type: Mapped[ItemType] = mapped_column(SQLEnum(ItemType), default=ItemType.TASK)
    status: Mapped[ItemStatus] = mapped_column(SQLEnum(ItemStatus), default=ItemStatus.INBOX)
    energy_level: Mapped[Optional[EnergyLevel]] = mapped_column(SQLEnum(EnergyLevel))
    time_estimate: Mapped[Optional[int]] = mapped_column(Integer)  # minutes
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime)
    remind_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    delegated_to: Mapped[Optional[str]] = mapped_column(String)
    review_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=datetime.utcnow,
        nullable=False
    )
    
    # Foreign keys
    area_id: Mapped[Optional[int]] = mapped_column(ForeignKey("areas.id", ondelete="SET NULL"))
    project_id: Mapped[Optional[int]] = mapped_column(ForeignKey("projects.id", ondelete="SET NULL"))
    context_id: Mapped[Optional[int]] = mapped_column(ForeignKey("contexts.id", ondelete="SET NULL"))
    
    # Relationships
    area = relationship("Area", back_populates="items")
    project = relationship("Project", back_populates="items")
    context = relationship("Context", back_populates="items")

    def __repr__(self) -> str:
        return f"<Item {self.id}: {self.title} ({self.status.value})>"
