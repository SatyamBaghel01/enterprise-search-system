from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class DocumentMetadata:
    source: str
    source_id: str
    title: str
    author: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    url: Optional[str] = None
    tags: Optional[List[str]] = None
    def to_dict(self) -> dict:
        data = asdict(self)
        if self.created_at:
            data["created_at"] = self.created_at.isoformat()
        return data
         
    # Optional, connector-specific fields
    issue_type: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    channel: Optional[str] = None
    thread_ts: Optional[str] = None
    file_type: Optional[str] = None

    extra: Optional[Dict[str, Any]] = None


@dataclass
class Document:
    content: str
    metadata: DocumentMetadata


class BaseConnector(ABC):
    def __init__(self, source_name: str):
        self.source_name = source_name

    @abstractmethod
    async def fetch_documents(self) -> List[Document]:
        """Fetch all documents from the source"""
        pass

    @abstractmethod
    async def fetch_document(self, document_id: str) -> Optional[Document]:
        """Fetch a single document by ID"""
        pass

    @abstractmethod
    async def search(self, query: str) -> List[Document]:
        """Search documents in the source"""
        pass
