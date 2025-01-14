"""GPT4ALL Backend Service."""
import os

from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.embeddings import GPT4AllEmbeddings
from langchain.vectorstores import Qdrant
from loguru import logger
from qdrant_client import QdrantClient
from qdrant_client.http import models

load_dotenv()

collection_name = "GPT4ALL"
data_folder = "resources/data"


def main():
    """Main function for the GPT4ALL ingestion service."""
    # Define the name of the collection you want to embedd the documents into.

    # this creates the collection if it does not exist
    qdrant_client = QdrantClient("http://qdrant", port=6333, api_key=os.getenv("QDRANT_API_KEY"), prefer_grpc=False)
    try:
        qdrant_client.get_collection(collection_name=collection_name)
        logger.info("SUCCESS: Collection already exists.")
    except Exception:
        qdrant_client.recreate_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
        )
        logger.info("SUCCESS: Collection created.")

    embedding = GPT4AllEmbeddings()

    vector_db = Qdrant(client=qdrant_client, collection_name="GPT4ALL", embeddings=embedding)

    # ingest text files
    ingest_text_files(dir=data_folder, vector_db=vector_db, file_ending="*.txt")

    # ingest pdfs
    ingest_pdfs_with_text(dir=data_folder, vector_db=vector_db)


def ingest_text_files(dir: str, vector_db: Qdrant, file_ending: str = "*.txt"):
    """Ingests text files from a directory."""
    loader = DirectoryLoader(dir, glob=file_ending, loader_cls=TextLoader)
    docs = loader.load()

    logger.info(f"Loaded {len(docs)} documents.")
    texts = [doc.page_content for doc in docs]
    metadatas = [doc.metadata for doc in docs]
    vector_db.add_texts(texts=texts, metadatas=metadatas)
    logger.info("SUCCESS: Texts embedded.")


def ingest_custom_text(text: str, seperator: str = "###"):
    """Ingests custom text."""
    pass


# ingest pdfs
def ingest_pdfs_with_text(dir: str, vector_db: Qdrant):
    """Ingests pdfs from a directory."""
    loader = DirectoryLoader(dir, glob="*.pdf", loader_cls=PyPDFLoader)
    docs = loader.load()

    logger.info(f"Loaded {len(docs)} documents.")
    texts = [doc.page_content for doc in docs]
    metadatas = [doc.metadata for doc in docs]
    vector_db.add_texts(texts=texts, metadatas=metadatas)
    logger.info("SUCCESS: Texts embedded.")


if __name__ == "__main__":
    main()
