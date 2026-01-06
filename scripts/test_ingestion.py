import asyncio
from datetime import datetime

from src.ingestion.pipeline import IngestionPipeline
from src.connectors.base import Document, DocumentMetadata


async def run_test():
    pipeline = IngestionPipeline()

    doc = Document(
        content=(
            "Enterprise search systems allow organizations to index, "
            "retrieve, and analyze information across multiple internal data sources. "
            "They typically use vector databases and large language models."
        ),
        metadata=DocumentMetadata(
            source="test",
            source_id="doc_001",
            title="Enterprise Search Overview",
            author="System",
            created_at=datetime.utcnow()
        )
    )

    result = await pipeline.ingest_documents([doc])
    print("Ingestion result:", result)


if __name__ == "__main__":
    asyncio.run(run_test())
