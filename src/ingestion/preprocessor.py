from typing import List, Dict
import re


class TextPreprocessor:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def clean_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def chunk_text(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        text = self.clean_text(text)
        chunks = []

        start = 0
        while start < len(text):
            end = start + self.chunk_size
            chunks.append(text[start:end])
            start = end - self.overlap

        return chunks

    def extract_metadata(self, text: str) -> Dict[str, str]:
        """Placeholder for NLP metadata extraction"""
        return {
            "length": str(len(text))
        }
