from config.settings import settings
from langchain_groq import ChatGroq

def get_llm(temperature: float = 0.2):
    if settings.LLM_PROVIDER == "groq":
        return ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model=settings.LLM_MODEL,
            temperature=temperature
        )

    raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")
