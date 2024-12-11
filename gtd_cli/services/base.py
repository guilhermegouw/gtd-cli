from typing import Generic, TypeVar, List, Optional, Type
from sqlalchemy.orm import Session
from ..db.base import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseService(Generic[ModelType]):
    """Base class for all services with common CRUD operations"""
    
    def __init__(self, db: Session, model: Type[ModelType]):
        """Initialize the service
        
        Args:
            db (Session): SQLAlchemy database session
            model (Type[ModelType]): SQLAlchemy model class
        """
        self.db = db
        self.model = model

    def get(self, id: int) -> Optional[ModelType]:
        """Get a single record by ID"""
        return self.db.query(self.model).filter(self.model.id == id).first()

    def get_all(self) -> List[ModelType]:
        """Get all records"""
        return self.db.query(self.model).all()

    def create(self, **kwargs) -> ModelType:
        """Create a new record"""
        obj = self.model(**kwargs)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        """Update a record by ID"""
        obj = self.get(id)
        if obj:
            for key, value in kwargs.items():
                setattr(obj, key, value)
            self.db.commit()
            self.db.refresh(obj)
        return obj

    def delete(self, id: int) -> bool:
        """Delete a record by ID"""
        obj = self.get(id)
        if obj:
            self.db.delete(obj)
            self.db.commit()
            return True
        return False
