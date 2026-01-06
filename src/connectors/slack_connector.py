from typing import List
from datetime import datetime
from .base import BaseConnector, Document, DocumentMetadata
import json
import os

class SlackConnector(BaseConnector):
    def __init__(self):
        super().__init__("slack")
        self.data_dir = "data/slack"
        
    async def fetch_documents(self) -> List[Document]:
        documents = []
        
        if not os.path.exists(self.data_dir):
            return documents
            
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    
                    metadata = DocumentMetadata(
                        source="slack",
                        source_id=data.get("id", filename),
                        title=f"#{data.get('channel', 'general')} - {data.get('timestamp', '')}",
                        author=data.get("user", "Unknown"),
                        created_at=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
                        updated_at=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
                        url=data.get("permalink"),
                        tags=[],
                        channel=data.get("channel", "general"),
                        thread_ts=data.get("thread_ts")
                    )
                    
                    document = Document(content=data.get("text", ""), metadata=metadata)
                    documents.append(document)
        
        return documents
    
    async def fetch_document(self, document_id: str) -> Document:
        return None
    
    async def search(self, query: str) -> List[Document]:
        all_docs = await self.fetch_documents()
        return [doc for doc in all_docs if query.lower() in doc.content.lower()]