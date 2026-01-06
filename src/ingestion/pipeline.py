from typing import List, Dict, Any
from .preprocessor import TextPreprocessor
from .embedder import Embedder
from ..connectors.base import Document
from ..storage.vector_store import VectorStore
from loguru import logger
import asyncio

class IngestionPipeline:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.embedder = Embedder()
        self.vector_store = VectorStore()
    
    async def process_document(self, document: Document) -> List[Dict[str, Any]]:
        """Process a single document through the pipeline"""
        try:
            # Chunk the document
            chunks = self.preprocessor.chunk_text(document.content)
            
            # Generate embeddings
            embeddings = self.embedder.embed_batch(chunks)
            
            # Prepare chunks with metadata
            processed_chunks = []
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_metadata = {
                    **document.metadata.to_dict(),
                    "chunk_index": idx,
                    "chunk_total": len(chunks),
                    **self.preprocessor.extract_metadata(chunk)
                }
                
                processed_chunks.append({
                    "id": f"{document.metadata.source_id}_chunk_{idx}",
                    "content": chunk,
                    "embedding": embedding,
                    "metadata": chunk_metadata
                })
            
            return processed_chunks
            
        except Exception as e:
            logger.error(f"Error processing document {document.metadata.source_id}: {e}")
            return []
    
    async def ingest_documents(self, documents: List[Document]) -> Dict[str, Any]:
        """Ingest multiple documents"""
        logger.info(f"Starting ingestion of {len(documents)} documents")
        
        all_chunks = []
        for document in documents:
            chunks = await self.process_document(document)
            all_chunks.extend(chunks)
        
        # Store in vector database
        if all_chunks:
            self.vector_store.add_documents(all_chunks)
            logger.info(f"Ingested {len(all_chunks)} chunks from {len(documents)} documents")
        
        return {
            "documents_processed": len(documents),
            "chunks_created": len(all_chunks),
            "status": "success"
        }