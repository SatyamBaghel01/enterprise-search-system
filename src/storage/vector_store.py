import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any
from config.settings import settings
from loguru import logger

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(
            settings=ChromaSettings(
                persist_directory=settings.CHROMA_PERSIST_DIR,
                #allow_reset=False,
                is_persistent=True,
                anonymized_telemetry=False
            )
        )
        
        self.collection_name = settings.CHROMA_COLLECTION
        self._initialize_collection()
    
    def _initialize_collection(self):
        """Initialize or get the collection"""
        try:
            try:
                self.collection = self.client.get_collection(name=self.collection_name)
            except Exception:
                self.collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Enterprise documents collection"}
                )
            logger.info(f"Initialized collection: {self.collection_name} | count={self.collection.count()}")
        except Exception as e:
            logger.error(f"Error initializing collection: {e}")
            raise
    
    def add_documents(self, chunks: List[Dict[str, Any]]):
        """Add document chunks to the vector store"""
        try:
            ids = [chunk["id"] for chunk in chunks]
            embeddings = [chunk["embedding"] for chunk in chunks]
            documents = [chunk["content"] for chunk in chunks]
            
            metadatas = []
            for chunk in chunks:
                clean_metadata = {
                    k: v
                    for k, v in chunk["metadata"].items()
                    if v is not None and isinstance(v, (str, int, float, bool))
                }
                metadatas.append(clean_metadata)

            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=documents,
                metadatas=metadatas
            )
            

            logger.info(f"Added {len(chunks)} chunks to vector store")

        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    
    def search(
        self,
        query_embedding: List[float],
        n_results: int = 10,
        where: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where,
                include=["documents", "metadatas", "distances"]
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results['ids'][0])):
                formatted_results.append({
                    "id": results['ids'][0][i],
                    "content": results['documents'][0][i],
                    "metadata": results['metadatas'][0][i],
                    "score": 1 - results['distances'][0][i]  # Convert distance to similarity
                })
            
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error searching: {e}")
            return []
    
    def delete_collection(self):
        """Delete the entire collection"""
        try:
            self.client.delete_collection(name=self.collection_name)
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")