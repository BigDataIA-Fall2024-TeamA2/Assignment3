from functools import lru_cache

from llama_index.core.base.embeddings.base import similarity
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.milvus import MilvusVectorStore

from backend.config import settings

CHAT_ENGINE_CACHE = {}
QA_LLM_SYSTEM_PROMPT = """
You are a multimodal assistant designed to efficiently answer user queries by retrieving relevant document excerpts. Only return the most
 relevant information instead of full documents, and combine text and image data for a comprehensive response.""".strip()


@lru_cache
def get_index(collection_name: str):
    return MilvusVectorStore(
        uri=settings.MILVUS_CLOUD_URI,
        token=settings.MILVUS_API_KEY,
        collection_name=collection_name,
    )


@lru_cache
def get_chat_engine(user_id: str):
    # if user_id not in CHAT_ENGINE_CACHE:
        index = get_index("idx")
        _llm = OpenAI(model="gpt-4o-mini", system_prompt=
        "You are a multimodal assistant designed to efficiently answer user queries by retrieving relevant document excerpts. Only return the most relevant information instead of full documents, and combine text and image data for a comprehensive response.")
        return index.as_chat_engine(similarity_top_k=10, llm=_llm, response_mode="")
    # return CHAT_ENGINE_CACHE[user_id]

