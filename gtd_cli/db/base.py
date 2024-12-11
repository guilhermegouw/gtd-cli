from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from pathlib import Path
import logging


logging.getLogger('sqlalchemy').setLevel(logging.WARNING)

# Get the project root directory
ROOT_DIR = Path(__file__).parent.parent.parent

# Database file path
DB_PATH = ROOT_DIR / "gtd.db"

class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    pass

# Create engine for SQLite database
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False)

Base.metadata.create_all(bind=engine)

# Create session factory
Session= sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db() -> Session:
    """Get database session"""
    session = Session()
    return session
