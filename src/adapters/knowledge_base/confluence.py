import datetime
import logging
from typing import List

from atlassian import Confluence
from atlassian.errors import ApiError
from pydantic import HttpUrl

from src.adapters.knowledge_base.base import BaseKnowledgeBaseConnector
from src.models.knowledge_base import KnowledgeBaseArticle

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ConfluenceConnector(BaseKnowledgeBaseConnector):
    """
    Connector for fetching articles from Confluence.
    """

    def __init__(self, url: str, api_key: str, space_key: str, username: str):
        self.url = url
        self.api_key = api_key
        self.space_key = space_key
        self.username = username
        self.confluence = Confluence(
            url=self.url, username=self.username, password=self.api_key, cloud=True
        )

    def _convert_to_article(self, content: dict) -> KnowledgeBaseArticle:
        """
        Converts a Confluence page content dictionary to a KnowledgeBaseArticle object.
        """
        article_url = f'{self.url.rstrip("/")}/wiki{content["_links"]["webui"]}'
        last_updated_str = content["version"]["when"]
        last_updated_dt = datetime.datetime.fromisoformat(
            last_updated_str.replace("Z", "+00:00")
        )
        return KnowledgeBaseArticle(
            id=content["id"],
            source="Confluence",
            title=content["title"],
            content=content["body"]["storage"]["value"],
            url=HttpUrl(article_url),
            service=content["space"]["key"],
            owner_team=content["space"]["name"],
            last_updated=last_updated_dt,
        )

    def fetch_articles(self) -> List[KnowledgeBaseArticle]:
        """
        Fetch articles from Confluence and return a list of KnowledgeBaseArticle objects.
        Handles errors gracefully if a page or the space is not found.
        """
        articles = []
        try:
            logger.info(f"Fetching pages from Confluence space: {self.space_key}...")
            pages = self.confluence.get_all_pages_from_space(self.space_key)
        except ApiError as e:
            logger.error(
                f"Error fetching pages from space '{self.space_key}': {e}. "
                f"Please check if the space exists and you have permissions."
            )
            return articles  # Return empty list if space is not accessible

        for page_summary in pages:
            page_id = page_summary["id"]
            try:
                content = self.confluence.get_page_by_id(
                    page_id, expand="body.storage,version,space"
                )

                if content is None:
                    continue

                article = self._convert_to_article(content)
                articles.append(article)

            except ApiError as e:
                logger.warning(
                    f"Could not fetch content for page ID '{page_id}'. Status: {e.args[0]}. Reason: {e.reason}. Skipping page."
                )
                continue  # Skip to the next page

        logger.info(f"Successfully fetched {len(articles)} articles from Confluence.")
        return articles
