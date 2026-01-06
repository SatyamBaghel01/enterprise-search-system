from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class SearchRequest(BaseModel):
    query: str = Field(..., description="Search query")
    sources: Optional[List[str]] = Field(None, description="Data sources to search")
    max_results: Optional[int] = Field(10, description="Maximum number of results")

class Citation(BaseModel):
    source_number: int
    source: str
    title: str
    url: Optional[str]
    excerpt: str

class DocumentResult(BaseModel):
    id: str
    source: str
    title: str
    excerpt: str
    score: float
    url: Optional[str]

class SearchResponse(BaseModel):
    query: str
    answer: str
    citations: List[Citation]
    confidence: float
    documents: List[DocumentResult]
    sources_searched: List[str]
    latency_ms: int
    query_analysis: Optional[Dict[str, Any]] = None

class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str