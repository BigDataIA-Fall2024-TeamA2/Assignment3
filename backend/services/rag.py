from functools import lru_cache

from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.base.embeddings.base import similarity
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.milvus import MilvusVectorStore

from backend.config import settings

CHAT_ENGINE_CACHE = {}
CHAT_LLM_SYSTEM_PROMPT = """You are a multimodal assistant designed to efficiently answer user queries by retrieving relevant document excerpts. Only return the most relevant information instead of full documents, and combine text and image data for a comprehensive response."""


@lru_cache
def get_index(collection_name: str) -> VectorStoreIndex:
    vector_store = MilvusVectorStore(
        uri=settings.MILVUS_CLOUD_URI,
        token=settings.MILVUS_API_KEY,
        collection_name=collection_name,
    )
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", embed_batch_size=100)
    return VectorStoreIndex.from_vector_store(vector_store=vector_store)


@lru_cache(maxsize=128)
def get_chat_engine(user_id: int, article_id: str, model: str = "gpt-4o"):
    index = get_index(settings.MILVUS_DOCUMENTS_COLLECTION)
    _llm = OpenAI(model=model, system_prompt="You are a multimodal assistant designed to efficiently answer user queries by retrieving relevant document excerpts. Only return the most relevant information instead of full documents, and combine text and image data for a comprehensive response.")
    return index.as_chat_engine(similarity_top_k=10, llm=_llm, response_mode="compact")
