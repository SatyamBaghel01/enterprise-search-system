from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from .llm_factory import get_llm
from config.settings import settings
from loguru import logger

class SynthesisAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.3)
    
    def synthesize_answer(
        self,
        query: str,
        retrieved_docs: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate answer from retrieved documents with citations"""
        
        if not retrieved_docs:
            return {
                "answer": "I couldn't find any relevant information to answer your question.",
                "citations": [],
                "confidence": 0.0
            }
        
        # Prepare context from retrieved documents
        context = self._prepare_context(retrieved_docs)
        
        prompt = ChatPromptTemplate.from_template("""
        You are an enterprise search assistant. Answer the question based ONLY on the provided context.
        Include specific references to sources by mentioning [Source N] where N is the source number.
        
        Context:
        {context}
        
        Question: {query}
        
        Provide a comprehensive answer with citations. Format citations as [Source 1], [Source 2], etc.
        
        Answer:
        """)
        
        try:
            ai_message = self.llm.invoke(
                prompt.format(context=context, query=query)
            )
            response = ai_message.content
            
            # Extract citations from response
            citations = self._extract_citations(response, retrieved_docs)
            
            return {
                "answer": response,
                "citations": citations,
                "confidence": self._calculate_confidence(retrieved_docs)
            }
            
        except Exception as e:
            logger.error(f"Error synthesizing answer: {e}")
            return {
                "answer": "An error occurred while generating the answer.",
                "citations": [],
                "confidence": 0.0
            }
    
    def _prepare_context(self, docs: List[Dict[str, Any]]) -> str:
        """Prepare context string from documents"""
        context_parts = []
        
        for idx, doc in enumerate(docs[:5], 1):  # Use top 5 results
            source_info = f"[Source {idx}] ({doc['metadata']['source']} - {doc['metadata']['title']})"
            content = doc['content'][:500]  # Limit content length
            context_parts.append(f"{source_info}\n{content}\n")
        
        return "\n".join(context_parts)
    
    def _extract_citations(
        self,
        answer: str,
        docs: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract citation information from answer"""
        citations = []
        
        import re
        citation_pattern = r'\[Source (\d+)\]'
        matches = re.findall(citation_pattern, answer)
        
        for match in set(matches):
            idx = int(match) - 1
            if idx < len(docs):
                doc = docs[idx]
                citations.append({
                    "source_number": int(match),
                    "source": doc["metadata"]["source"],
                    "title": doc["metadata"]["title"],
                    "url": doc["metadata"].get("url"),
                    "excerpt": doc["content"][:200]
                })
        
        return citations
    
    def _calculate_confidence(self, docs: List[Dict[str, Any]]) -> float:
        """Calculate confidence score based on retrieval quality"""
        if not docs:
            return 0.0
        
        avg_score = sum(doc["score"] for doc in docs) / len(docs)
        return min(avg_score, 1.0)