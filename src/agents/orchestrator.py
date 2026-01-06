from typing import Dict, Any, List
from .query_agent import QueryAgent
from .retrieval_agent import RetrievalAgent
from .synthesis_agent import SynthesisAgent
from ..storage.metadata_store import MetadataStore
from loguru import logger
import time

class SearchOrchestrator:
    """Main orchestrator for the agentic search system"""
    
    def __init__(self):
        self.query_agent = QueryAgent()
        self.retrieval_agent = RetrievalAgent()
        self.synthesis_agent = SynthesisAgent()
        #self.metadata_store = MetadataStore()
        self.metadata_store = None
    
    def search(
        self,
        query: str,
        sources: List[str] = None,
        max_results: int = 10
    ) -> Dict[str, Any]:
        """Execute complete search workflow"""
        
        start_time = time.time()
        
        try:
            # Step 1: Analyze query
            logger.info(f"Analyzing query: {query}")
            query_analysis = self.query_agent.analyze_query(query)
            
            # Determine sources
            if sources:
                search_sources = sources
            else:
                search_sources = query_analysis["sources"]
                if "all" in search_sources:
                    search_sources = ["confluence", "jira", "slack", "documents"]
            
            # Step 2: Retrieve relevant documents
            logger.info(f"Retrieving from sources: {search_sources}")
            retrieved_docs = self.retrieval_agent.retrieve(
                query=query_analysis["reformulated_query"],
                sources=search_sources,
                max_results=max_results
            )
            
            # Step 3: Synthesize answer
            logger.info(f"Synthesizing answer from {len(retrieved_docs)} documents")
            result = self.synthesis_agent.synthesize_answer(
                query=query,
                retrieved_docs=retrieved_docs
            )
            
            # Calculate latency
            latency_ms = int((time.time() - start_time) * 1000)
            
            # Log query
            # self.metadata_store.log_query(
            #     query=query,
            #     results_count=len(retrieved_docs),
            #     latency_ms=latency_ms,
            #     sources=search_sources
            # )
            
            # Build final response
            response = {
                "query": query,
                "query_analysis": query_analysis,
                "answer": result["answer"],
                "citations": result["citations"],
                "confidence": result["confidence"],
                "documents": [
                    {
                        "id": doc["id"],
                        "source": doc["metadata"]["source"],
                        "title": doc["metadata"]["title"],
                        "excerpt": doc["content"][:200],
                        "score": doc["score"],
                        "url": doc["metadata"].get("url")
                    }
                    for doc in retrieved_docs
                ],
                "sources_searched": search_sources,
                "latency_ms": latency_ms
            }
            
            logger.info(f"Search completed in {latency_ms}ms")
            return response
            
        except Exception as e:
            logger.error(f"Error in search orchestration: {e}")
            return {
                "query": query,
                "answer": f"An error occurred: {str(e)}",
                "citations": [],
                "confidence": 0.0,
                "documents": [],
                "sources_searched": sources or [],
                "latency_ms": int((time.time() - start_time) * 1000)
            }