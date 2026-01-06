from typing import List
from datetime import datetime
from .base import BaseConnector, Document, DocumentMetadata
import os
from pathlib import Path

class DocumentConnector(BaseConnector):
    def __init__(self):
        super().__init__("documents")
        self.data_dir = "data/documents"
        
    async def fetch_documents(self) -> List[Document]:
        documents = []
        
        if not os.path.exists(self.data_dir):
            return documents
            
        for filepath in Path(self.data_dir).rglob('*.txt'):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
                stat = os.stat(filepath)
                created_at = datetime.fromtimestamp(stat.st_ctime)
                updated_at = datetime.fromtimestamp(stat.st_mtime)
                
                metadata = DocumentMetadata(
                    source="documents",
                    source_id=str(filepath),
                    title=filepath.stem,
                    author="System",
                    created_at=created_at,
                    updated_at=updated_at,
                    url=f"file://{filepath}",
                    tags=[],
                    file_type=filepath.suffix
                )
                
                document = Document(content=content, metadata=metadata)
                documents.append(document)
        
        return documents
    
    async def fetch_document(self, document_id: str) -> Document:
        return None
    
    async def search(self, query: str) -> List[Document]:
        all_docs = await self.fetch_documents()
        return [doc for doc in all_docs if query.lower() in doc.content.lower()]