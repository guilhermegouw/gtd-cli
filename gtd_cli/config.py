from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

# Database
DATABASE_URL = f"sqlite:///{BASE_DIR}/gtd.db"

# Application settings
DEBUG = True
