from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_parse import LlamaParse

def get_embedding_model():
    return OpenAIEmbedding(model="text-embedding-3-small")


def get_parser():
    return LlamaParse(
        result_type="markdown",
        use_vendor_multimodal_model=True,
        vendor_multimodal_model_name="openai-gpt4o"
    )