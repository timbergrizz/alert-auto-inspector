from abc import ABC, abstractmethod
from typing import List
from src.models.knowledge_base import KnowledgeBaseArticle

class BaseKnowledgeBaseConnector(ABC):
    """
    Abstract base class for knowledge base connectors.
    """

    @abstractmethod
    def fetch_articles(self) -> List[KnowledgeBaseArticle]:
        """
        Fetch articles from the knowledge base and return a list of KnowledgeBaseArticle objects.
        """
        pass
