import os

from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings, StorageContext, VectorStoreIndex
from dotenv import load_dotenv
from llama_index.vector_stores.milvus import MilvusVectorStore

from dags.articles import get_all_articles
from dags.data_indexer.document_processors import load_data_from_directory
from dags.data_ingestion.utils import fetch_file_from_s3, ensure_resource_dir_exists, CACHED_RESOURCES_PATH

load_dotenv()

def _fetch_files_from_s3(article_id: str, pdf_s3_key: str, image_s3_key: str):
    fetch_file_from_s3(pdf_s3_key, os.path.join("pdfs", str(article_id)))
    fetch_file_from_s3(image_s3_key, os.path.join("images", str(article_id)))


def create_index(documents):
    milvus_uri = os.getenv("MILVUS_CLOUD_URI")
    milvus_key = os.getenv("MILVUS_API_KEY")
    vector_store = MilvusVectorStore(
        uri=milvus_uri,
        token=milvus_key,
        collection_name="DocumentsIndex",
    )
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_documents(documents, storage_context=storage_context)


def index_document():
    Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", embed_batch_size=100)
    Settings.llm = OpenAI(model="gpt-4o-mini", temperature=0.1)
    Settings.text_splitter = SentenceSplitter(chunk_size=600)

    ensure_resource_dir_exists()
    articles = get_all_articles()
    for article in articles:
        _fetch_files_from_s3(article[0], article[1], article[2])
    documents = load_data_from_directory(os.path.join(CACHED_RESOURCES_PATH, "pdfs"))

    print(len(documents))

    index = create_index(documents)


if __name__ == '__main__':
    index_document()
