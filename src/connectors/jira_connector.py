from typing import List
from datetime import datetime
from .base import BaseConnector, Document, DocumentMetadata
import json
import os

class JiraConnector(BaseConnector):
    def __init__(self):
        super().__init__("jira")
        self.data_dir = "data/jira"
        
    async def fetch_documents(self) -> List[Document]:
        documents = []
        
        if not os.path.exists(self.data_dir):
            return documents
            
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.data_dir, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    
                    content = f"""
                    Issue: {data.get('title', 'Untitled')}
                    Description: {data.get('description', '')}
                    Status: {data.get('status', 'Unknown')}
                    Priority: {data.get('priority', 'Medium')}
                    Assignee: {data.get('assignee', 'Unassigned')}
                    Comments: {data.get('comments', '')}
                    """
                    
                    metadata = DocumentMetadata(
                        source="jira",
                        source_id=data.get("id", filename),
                        title=data.get("title", "Untitled"),
                        author=data.get("reporter", "Unknown"),
                        created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
                        updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
                        url=data.get("url"),
                        tags=data.get("labels", []),
                        issue_type=data.get("issue_type", "Task"),
                        status=data.get("status", "Open"),
                        priority=data.get("priority", "Medium")
                    )
                    
                    document = Document(content=content.strip(), metadata=metadata)
                    documents.append(document)
        
        return documents
    
    async def fetch_document(self, document_id: str) -> Document:
        filepath = os.path.join(self.data_dir, f"{document_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
                # Implement similar to fetch_documents
                pass
        return None
    
    async def search(self, query: str) -> List[Document]:
        all_docs = await self.fetch_documents()
        return [doc for doc in all_docs if query.lower() in doc.content.lower()]