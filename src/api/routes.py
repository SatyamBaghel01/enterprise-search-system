from fastapi import APIRouter, HTTPException, Query
from .models import SearchRequest, SearchResponse, HealthResponse
from ..agents.orchestrator import SearchOrchestrator
from typing import List
from loguru import logger

router = APIRouter()
orchestrator = SearchOrchestrator()

@router.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    """
    Execute intelligent search across enterprise data sources
    """
    try:
        result = orchestrator.search(
            query=request.query,
            sources=request.sources,
            max_results=request.max_results
        )
        return result
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sources")
async def get_sources():
    """
    Get available data sources
    """
    return {
        "sources": [
            {
                "id": "confluence",
                "name": "Confluence",
                "description": "Wiki and documentation",
                "icon": "📚"
            },
            {
                "id": "jira",
                "name": "Jira",
                "description": "Project management and issues",
                "icon": "🎯"
            },
            {
                "id": "slack",
                "name": "Slack",
                "description": "Team communications",
                "icon": "💬"
            },
            {
                "id": "documents",
                "name": "Documents",
                "description": "File storage",
                "icon": "📁"
            }
        ]
    }

@router.get("/stats")
async def get_stats():
    """
    Get system statistics
    """
    # This is simplified - in production, get real stats
    return {
        "total_documents": 150,
        "total_chunks": 450,
        "sources_connected": 4,
        "queries_today": 47,
        "avg_latency_ms": 523
    }