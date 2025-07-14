import logging
from typing import List

import chromadb
from chromadb.utils import embedding_functions

from core.config import DB_PATH, DB_COLLECTION_NAME
from models.knowledge_base import KnowledgeBaseArticle

# Configure logging
logger = logging.getLogger(__name__)


class VectorDBService:
    """
    A service to interact with a ChromaDB vector database.
    This service is responsible for initializing the database client,
    managing collections, and handling document operations like
    adding, upserting, and querying.
    """

    def __init__(self, db_path: str = DB_PATH, collection_name: str = DB_COLLECTION_NAME):
        """
        Initializes the VectorDBService.

        Args:
            db_path (str): The file path to the persistent ChromaDB database.
            collection_name (str): The name of the collection to interact with.
        """
        try:
            self.client = chromadb.PersistentClient(path=db_path)
            self.embedding_function = (
                embedding_functions.SentenceTransformerEmbeddingFunction(
                    model_name="all-MiniLM-L6-v2"
                )
            )
            self.collection = self.client.get_or_create_collection(
                name=collection_name, embedding_function=self.embedding_function
            )
            logger.info(
                f"VectorDBService initialized. Collection '{collection_name}' is ready."
            )
        except Exception as e:
            logger.exception(
                f"Failed to initialize ChromaDB client at path '{db_path}'. Error: {e}"
            )
            raise

    def add_documents(self, articles: List[KnowledgeBaseArticle]):
        """
        Adds or updates a list of KnowledgeBaseArticle objects in the collection.

        This method is idempotent. If a document with the same ID already exists,
        it will be updated (upserted).

        Args:
            articles (List[KnowledgeBaseArticle]): A list of articles to add/update.
        """
        if not articles:
            logger.warning("No articles provided to add_documents. Skipping.")
            return

        ids = [article.id for article in articles]
        documents = [article.content for article in articles]
        metadatas = [
            article.model_dump(exclude={"id", "content"}) for article in articles
        ]

        try:
            # Use upsert for idempotency
            self.collection.upsert(ids=ids, documents=documents, metadatas=metadatas)
            logger.info(f"Successfully upserted {len(articles)} documents.")
        except Exception as e:
            logger.exception(f"Failed to upsert documents into ChromaDB. Error: {e}")
            # Depending on the use case, you might want to handle this more gracefully
            # or re-raise the exception to signal a failure in the ingestion pipeline.
            raise

    def query_documents(self, query_texts: List[str], n_results: int = 5) -> List[dict]:
        """
        Queries the collection for documents similar to the query texts.

        Args:
            query_texts (List[str]): The text(s) to search for.
            n_results (int): The number of results to return per query.

        Returns:
            List[dict]: A list of query results.
        """
        if not self.collection:
            raise ValueError(
                "Collection not initialized. The service may not have been created properly."
            )

        try:
            results = self.collection.query(
                query_texts=query_texts, n_results=n_results
            )
            return results
        except Exception as e:
            logger.exception(f"Failed to query documents from ChromaDB. Error: {e}")
            raise
