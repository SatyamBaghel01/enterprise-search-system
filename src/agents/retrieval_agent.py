from typing import List, Dict, Any
from ..storage.vector_store import VectorStore
from ..ingestion.embedder import Embedder
from config.settings import settings
from loguru import logger

class RetrievalAgent:
    def __init__(self):
        self.vector_store = VectorStore()
        self.embedder = Embedder()
    
    def retrieve(
        self,
        query: str,
        sources: List[str] = None,
        max_results: int = None
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant documents using hybrid search"""
        
        max_results = max_results or settings.MAX_RESULTS
        
        try:
            # Generate query embedding
            query_embedding = self.embedder.embed_text(query)
            
            # Build filter for sources
            where_filter = None
            if sources and "all" not in sources:
                where_filter = {"source": {"$in": sources}}
            
            # Perform vector search
            results = self.vector_store.search(
                query_embedding=query_embedding,
                n_results=max_results * 2,  # Get more for reranking
                where=where_filter
            )
            
            # Filter by similarity threshold
            # filtered_results = [
            #     r for r in results
            #     if r["score"] >= settings.SIMILARITY_THRESHOLD
            # ]
            filtered_results = results
            
            # Rerank and deduplicate
            reranked_results = self._rerank(query, filtered_results)
            
            return reranked_results[:max_results]
            
        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            return []
    
    def _rerank(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Reranking based on exact match and recency"""
        
        query_lower = query.lower()
        
        for result in results:
            # Boost exact matches
            if query_lower in result["content"].lower():
                result["score"] += 0.1
            
            # Boost recent documents
            if "updated_at" in result["metadata"]:
                # This is simplified - in production use proper date parsing
                result["score"] += 0.05
        
        # Sort by score
        return sorted(results, key=lambda x: x["score"], reverse=True)