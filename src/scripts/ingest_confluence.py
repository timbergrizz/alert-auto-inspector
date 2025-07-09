
import logging
import os
from typing import List, Protocol

from dotenv import load_dotenv

from adapters.knowledge_base.base import BaseKnowledgeBaseConnector
from adapters.knowledge_base.confluence import ConfluenceConnector
from models.knowledge_base import KnowledgeBaseArticle
from services.vector_db_service import VectorDBService

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class IngestionPipeline(Protocol):
    """
    A protocol defining the interface for an ingestion pipeline.
    This allows for different types of pipelines (e.g., Confluence, Git)
    to be used interchangeably.
    """

    def run(self) -> None:
        ...


class ConfluenceIngestionPipeline:
    """
    A pipeline for ingesting knowledge base articles from Confluence
    and storing them in a vector database.
    """

    def __init__(
        self, connector: BaseKnowledgeBaseConnector, db_service: VectorDBService
    ):
        self.connector = connector
        self.db_service = db_service

    def run(self) -> None:
        """
        Executes the ingestion pipeline.
        1. Fetches articles from the source.
        2. Upserts them into the vector database.
        """
        logger.info("Starting ingestion pipeline...")
        try:
            articles = self._fetch_articles()
            if articles:
                self._store_articles(articles)
                logger.info(f"Successfully processed {len(articles)} articles.")
            else:
                logger.info("No articles found to process.")
        except Exception as e:
            logger.exception(f"An error occurred during the ingestion pipeline: {e}")
            # In a real-world scenario, you might want to raise the exception
            # to signal a failure to the calling process (e.g., a CI/CD job).
            raise

        logger.info("Ingestion pipeline finished.")

    def _fetch_articles(self) -> List[KnowledgeBaseArticle]:
        """Fetches articles using the configured connector."""
        logger.info("Fetching articles from the knowledge base...")
        return self.connector.fetch_articles()

    def _store_articles(self, articles: List[KnowledgeBaseArticle]) -> None:
        """Stores articles in the vector database."""
        logger.info(f"Storing {len(articles)} articles in the vector database...")
        # The add_documents method in VectorDBService should handle upserting
        # to ensure idempotency.
        self.db_service.add_documents(articles)
        logger.info("Finished storing articles.")


def main():
    """
    Main function to set up and run the ingestion pipeline.
    """
    # Load environment variables from .env file for local development
    load_dotenv()

    # --- Configuration ---
    # It's recommended to use environment variables for configuration
    # to keep the script flexible and secure.
    confluence_url = os.getenv("CONFLUENCE_URL", "")
    confluence_api_key = os.getenv("CONFLUENCE_API_KEY", "")
    confluence_space_key = os.getenv("CONFLUENCE_SPACE_KEY", "")
    confluence_username = os.getenv("CONFLUENCE_USERNAME", "")
    chroma_db_path = os.getenv("CHROMA_DB_PATH", "./src/chroma_db")
    collection_name = os.getenv("CHROMA_COLLECTION_NAME", "knowledge_base")

    # --- Dependency Injection ---
    # Initialize the necessary components and inject them into the pipeline.
    # This makes the pipeline more modular and easier to test.

    # 1. Set up the Knowledge Base Connector
    # This could be easily swapped out for a different connector,
    # e.g., GitConnector, NotionConnector.
    try:
        connector = ConfluenceConnector(
            url=confluence_url,
            api_key=confluence_api_key,
            space_key=confluence_space_key,
            username=confluence_username,
        )
    except Exception as e:
        logger.error(f"Failed to initialize ConfluenceConnector: {e}")
        return

    # 2. Set up the Vector Database Service
    try:
        db_service = VectorDBService(
            db_path=chroma_db_path, collection_name=collection_name
        )
    except Exception as e:
        logger.error(f"Failed to initialize VectorDBService: {e}")
        return

    # 3. Set up and run the pipeline
    pipeline: IngestionPipeline = ConfluenceIngestionPipeline(
        connector=connector, db_service=db_service
    )
    pipeline.run()


if __name__ == "__main__":
    main()
