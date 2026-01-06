import asyncio
import sys
sys.path.append('.')

#from src.connectors.confluence_connector import ConfluenceConnector
from src.connectors.jira_connector import JiraConnector
from src.connectors.slack_connector import SlackConnector
from src.connectors.document_connector import DocumentConnector
from src.ingestion.pipeline import IngestionPipeline
from loguru import logger

async def main():
    """Ingest all data from connectors"""
    
    logger.info("Starting data ingestion pipeline...")
    
    # Initialize pipeline
    pipeline = IngestionPipeline()
    
    # Initialize connectors
    connectors = [
       # ConfluenceConnector(),
        JiraConnector(),
        SlackConnector(),
        DocumentConnector()
    ]
    
    total_docs = 0
    
    for connector in connectors:
        logger.info(f"Fetching documents from {connector.source_name}...")
        
        try:
            documents = await connector.fetch_documents()
            logger.info(f"Found {len(documents)} documents from {connector.source_name}")
            
            if documents:
                result = await pipeline.ingest_documents(documents)
                logger.info(f"Ingested {result['chunks_created']} chunks from {result['documents_processed']} documents")
                total_docs += result['documents_processed']
        
        except Exception as e:
            logger.error(f"Error ingesting from {connector.source_name}: {e}")
    
    logger.info(f" Ingestion complete! Total documents: {total_docs}")

if __name__ == "__main__":
    asyncio.run(main())