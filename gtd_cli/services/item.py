from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime

from .base import BaseService
from ..db.models import Item, ItemType, ItemStatus
from ..exceptions import ValidationError


class ItemService(BaseService[Item]):
    def __init__(self, db: Session):
        super().__init__(db=db, model=Item)  # Fixed parameter order
    
    def create_inbox_item(self, title: str, description: str = "") -> Item:
        """Create a new inbox item"""
        if not title:
            raise ValidationError("Title cannot be empty")
            
        return self.create(
            title=title,
            description=description,
            type=ItemType.TASK,
            status=ItemStatus.INBOX,
            created_at=datetime.utcnow()
        )
    
    def get_inbox_items(self) -> List[Item]:
        """Get all inbox items"""
        return (
            self.db.query(Item)
            .filter(Item.status == ItemStatus.INBOX)
            .order_by(Item.created_at.desc())
            .all()
        )
