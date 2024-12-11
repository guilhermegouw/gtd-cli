import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gtd_cli.db.base import Base

@pytest.fixture(scope="session")
def engine():
    """Create a test database engine."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return engine

@pytest.fixture
def db_session(engine):
    """Create a fresh test database session."""
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.rollback()
        session.close()

@pytest.fixture
def sample_item():
    """Fixture to provide a sample inbox item."""
    return {
        "title": "Test Task",
        "description": "Test Description",
    }

@pytest.fixture
def sample_item_empty_description():
    """Fixture to provide a sample inbox item with empty description"""
    return {
        "title": "Test Task",
        "description": "",
    }
