from typing import Dict, List, Any
from langchain_core.prompts import ChatPromptTemplate
from  .llm_factory import get_llm
from config.settings import settings
from loguru import logger
import re

class QueryAgent:
    def __init__(self):
        self.llm = get_llm(temperature=0.1)
    
    def analyze_query(self, query: str) -> Dict[str, Any]:
        """Analyze the user query to extract intent and context"""
        
        prompt = ChatPromptTemplate.from_template("""
        Analyze the following user query and extract:
        1. Primary intent (search, question, summary, comparison)
        2. Key entities mentioned
        3. Relevant data sources (confluence, jira, slack, documents)
        4. Time constraints if any
        5. Reformulated query for better search
        
        Query: {query}
        
        Respond in this format:
        INTENT: <intent>
        ENTITIES: <comma-separated entities>
        SOURCES: <comma-separated sources>
        TIME: <time constraint or "none">
        REFORMULATED: <better query>
        """)
        
        try:
            ai_message = self.llm.invoke(prompt.format(query=query))
            response = ai_message.content


            # Parse response
            intent_match = re.search(r'INTENT:\s*(.+)', response)
            entities_match = re.search(r'ENTITIES:\s*(.+)', response)
            sources_match = re.search(r'SOURCES:\s*(.+)', response)
            time_match = re.search(r'TIME:\s*(.+)', response)
            reformulated_match = re.search(r'REFORMULATED:\s*(.+)', response)
            if not response.strip():
                raise ValueError("Empty LLM response")            
            return {
                "original_query": query,
                "intent": intent_match.group(1).strip() if intent_match else "search",
                "entities": [e.strip() for e in entities_match.group(1).split(",")] if entities_match else [],
                "sources": [s.strip() for s in sources_match.group(1).split(",")] if sources_match else ["all"],
                "time_constraint": time_match.group(1).strip() if time_match else None,
                "reformulated_query": reformulated_match.group(1).strip() if reformulated_match else query
            }
            
        except Exception as e:
            logger.error(f"Error analyzing query: {e}")
            return {
                "original_query": query,
                "intent": "search",
                "entities": [],
                "sources": ["all"],
                "time_constraint": None,
                "reformulated_query": query
            }