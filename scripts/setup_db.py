import sys
sys.path.append('.')

from src.storage.metadata_store import MetadataStore, Base
from sqlalchemy import create_engine
from config.settings import settings
from loguru import logger

def setup_database():
    """Initialize the database"""
    
    logger.info("Setting up database...")
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(engine)
        logger.info("✅ Database tables created successfully")
        
        # Test connection
        metadata_store = MetadataStore()
        logger.info("✅ Database connection verified")
        
    except Exception as e:
        logger.error(f"❌ Error setting up database: {e}")
        raise

if __name__ == "__main__":
    setup_database()