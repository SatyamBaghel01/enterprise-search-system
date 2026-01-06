from sqlalchemy import create_engine, Column, String, DateTime, Integer, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config.settings import settings

Base = declarative_base()

class DocumentMetadataModel(Base):
    __tablename__ = "document_metadata"
    
    id = Column(String, primary_key=True)
    source = Column(String, index=True)
    source_id = Column(String, index=True)
    title = Column(String)
    author = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    url = Column(String, nullable=True)
    tags = Column(JSON)
    extra_metadata = Column(JSON)
    indexed_at = Column(DateTime, default=datetime.utcnow)

class QueryLog(Base):
    __tablename__ = "query_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    query = Column(Text)
    user_id = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    results_count = Column(Integer)
    latency_ms = Column(Integer)
    sources_used = Column(JSON)

class MetadataStore:
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self):
        return self.SessionLocal()
    
    def log_query(self, query: str, results_count: int, latency_ms: int, sources: list):
        session = self.get_session()
        try:
            log = QueryLog(
                query=query,
                results_count=results_count,
                latency_ms=latency_ms,
                sources_used=sources
            )
            session.add(log)
            session.commit()
        finally:
            session.close()